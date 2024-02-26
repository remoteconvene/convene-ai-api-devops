import uuid

import structlog
from fastapi import Request
from fastapi import status
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import MongoDBChatMessageHistory
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import Tool

from src.apis.v1.enums.query_type import QueryType
from src.apis.v1.enums.token_data import TokenData
from src.apis.v1.models.message import CreateMessage
from src.apis.v1.models.source import CreateSource
from src.apis.v1.models.thread import ChatHistoryRequest
from src.apis.v1.models.thread import CreateThread
from src.apis.v1.models.thread import ImageQueryRequest
from src.apis.v1.models.thread import QueryResponse
from src.apis.v1.models.thread import SourceResponse
from src.apis.v1.models.thread import TextQueryRequest
from src.apis.v1.service.consumer_token import get_token_detail
from src.core.config.settings import settings
from src.core.db.models.thread import Thread
from src.core.db.repositories.file import get_image_base64
from src.core.db.repositories.message import add_new_message_to_thread
from src.core.db.repositories.thread import add_new_thread
from src.core.db.repositories.thread import close_thread_by_thread_id_repo
from src.core.db.repositories.thread import get_thread_by_thread_id
from src.core.db.repositories.thread import get_threads_repo
from src.core.langchain.openai import get_openai_vision_answer
from src.core.langchain.openai_config import get_chat_openai
from src.core.utils.custom_errors import InvalidUuidError
from src.core.utils.error_messages import errors
from src.core.utils.messages import messages
from src.core.utils.strings_constants import constants
from src.core.utils.throw_error import raise_error
from src.core.utils.token_size import get_token_from_header
from src.core.utils.token_size import get_token_size
from src.core.utils.validators import validate_uuid
from src.core.vector_db.chroma_db import get_vector_db

logger = structlog.get_logger()


def get_threads_ser():
    return get_threads_repo()


def get_thread_by_thread_id_ser(thread_id: str):
    return get_thread_by_thread_id(thread_id)


def close_thread_by_thread_id_ser(thread_id: str):
    close_thread_by_thread_id_repo(thread_id)


def process_input_with_result(data, config):
    query = data["query"]
    answer = data["result"]
    thread_id = config["configurable"]["session_id"]

    chat_history = MongoDBChatMessageHistory(
        session_id=thread_id,
        connection_string=settings.MONGODB_URL,
        database_name=settings.MONGODB_DATABASE,
        collection_name="chat_histories",
    )

    chat_history.add_user_message(query)
    chat_history.add_ai_message(answer)

    return {"question": query, "answer": answer, "history": chat_history}


def get_openai_answer_v1(query: str, thread_id: str):
    # TODO Need to change later to the actual path of chroma DB
    # persist_directory = "E:/Workspace/convene-ai-api/chroma_esg_db/"
    # embedding = OpenAIEmbeddings()
    # vectordb = Chroma(persist_directory=persist_directory,
    # embedding_function=embedding)

    llm = ChatOpenAI(
        model_name=settings.OPENAI_LLM_MODEL, temperature=settings.OPENAI_LLM_TEMP
    )

    # llm_chain = prompt | llm  # Pass the prompt to ChatOpenAI

    # qa_chain = RetrievalQA.from_chain_type(
    #     llm=llm, retriever=vectordb.as_retriever(), return_source_documents=True
    # )

    # result = qa_chain.invoke({"query": query})

    # chain = qa_chain | process_input_with_result

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )

    chain = prompt | llm

    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: MongoDBChatMessageHistory(
            session_id=thread_id,
            connection_string=settings.MONGODB_URL,
            database_name=settings.MONGODB_DATABASE,
            collection_name="chat_histories",
        ),
        input_messages_key="question",
        # output_messages_key="answer",
        history_messages_key="history",
    )

    config = {"configurable": {"session_id": thread_id}}

    output = chain_with_history.invoke({"question": query}, config=config)

    return output["answer"]


def get_openai_answer(query: str, thread_id: str):
    chat_message_history = MongoDBChatMessageHistory(
        session_id=thread_id,
        connection_string=settings.MONGODB_URL,
        database_name=settings.MONGODB_DATABASE,
        collection_name=settings.MONGODB_CHAT_HISTORY_COLLECTION,
    )

    chat_history = chat_message_history.messages

    memory = ConversationBufferMemory(
        memory_key=constants.CHAT_HISTORY,
        chat_memory=chat_message_history,
        input_key=constants.INPUT_KEY,
        output_key=constants.OUTPUT_KEY,
    )

    message_array = [
        SystemMessagePromptTemplate.from_template(messages.SYSTEM_MESSAGE_TEMPLATE),
        HumanMessagePromptTemplate.from_template(messages.USER_MESSAGE_TEMPLATE),
    ]
    qa_prompt = ChatPromptTemplate.from_messages(message_array)

    llm = get_chat_openai()

    retriever = get_vector_db().as_retriever(search_type="mmr", search_kwargs={"k": 2})

    def get_chat_history(context):
        chat_history_mapping = {i: message for i, message in enumerate(chat_history)}
        return chat_history_mapping

    qa = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        verbose=False,
        memory=memory,
        get_chat_history=get_chat_history,
        chain_type=constants.CHAIN_TYPE,
        combine_docs_chain_kwargs={constants.PROMPT: qa_prompt},
        return_source_documents=True,
    )

    result = qa.invoke({constants.INPUT_KEY: query})

    return result


def get_openai_answer_v3(query: str, thread_id: str):
    vectordb = get_vector_db()
    llm = get_chat_openai()

    chat_message_history = MongoDBChatMessageHistory(
        session_id=thread_id,
        connection_string=settings.MONGODB_URL,
        database_name=settings.MONGODB_DATABASE,
        collection_name="chat_histories",
    )

    # chat_history = chat_message_history.messages

    # chat_history_mapping = {i: message for i, message in enumerate(chat_history)}

    memory = ConversationBufferMemory(
        chat_memory=chat_message_history,
        memory_key="chat_history",
        return_messages=True,
    )

    retriever = vectordb.as_retriever()

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        # return_source_documents=True
    )

    tools = [
        Tool.from_function(
            func=qa_chain.run,
            name="Reader",
            description="useful for when we need to answer question from context",
        )
    ]

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
    )

    answer = agent.run(input=query)

    return answer


def get_create_sources(sources: list):
    create_sources = []
    for source in sources:
        metadata = source.metadata
        create_source = CreateSource(title=metadata["name"], url=metadata["file_path"])
        create_sources.append(create_source)

    return create_sources


def get_create_message(
    query: str,
    answer: str,
    query_type: str,
    sources: list,
    thread_id: int = None,
    file_id: int = None,
):
    query_token_size = get_token_size(query)
    answer_token_size = get_token_size(answer)
    ai_response_token_size = query_token_size + answer_token_size

    return CreateMessage(
        thread_id=thread_id,
        file_id=file_id,
        query=query,
        answer=answer,
        query_token_size=query_token_size,
        answer_token_size=answer_token_size,
        ai_response_token_size=ai_response_token_size,
        query_type=query_type,
        sources=get_create_sources(sources),
    )


def get_thread_response(thread_id: str, answer: str, sources: list):
    source_responses = []
    for source in sources:
        source_response = SourceResponse(title=source.title, url=source.url)
        source_responses.append(source_response)

    return QueryResponse(thread_id=thread_id, response=answer, sources=source_responses)


def text_query_ser(text_query_req: TextQueryRequest, request: Request):
    if text_query_req.thread_id is None:
        thread_id = str(uuid.uuid4())
        token = get_token_from_header(request)
        data = get_token_detail(token)
        result = get_openai_answer(text_query_req.query, thread_id)
        answer: str = result["answer"]
        sources: list = result["source_documents"]

        new_thread = CreateThread(
            thread_id=thread_id,
            external_user_id=data[TokenData.EXTERNAL_USER_ID],
            consumer_id=data[TokenData.CONSUMER_ID],
            messages=[
                get_create_message(
                    text_query_req.query, answer, QueryType.TEXT.value, sources
                )
            ],
        )

        add_new_thread(new_thread)

        thread_response = get_thread_response(
            thread_id, answer, new_thread.messages[0].sources
        )

        return thread_response
    else:
        try:
            validate_uuid(text_query_req.thread_id)
            result = get_openai_answer(text_query_req.query, text_query_req.thread_id)
            answer: str = result["answer"]
            sources: list = result["source_documents"]

            db_thread: Thread = get_thread_by_thread_id(text_query_req.thread_id)

            message = get_create_message(
                text_query_req.query,
                answer,
                QueryType.TEXT.value,
                sources,
                db_thread.id,
            )

            add_new_message_to_thread(message)

            thread_response = get_thread_response(
                text_query_req.thread_id, answer, message.sources
            )

            return thread_response
        except InvalidUuidError as e:
            error_message = e.args[0]
            logger.error(error_message)

            raise raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=errors.INVALID_THREAD_ID,
            )


def image_query_ser(
    image_query_req: ImageQueryRequest,
    request: Request = None,
):
    token = get_token_from_header(request)
    data = get_token_detail(token)

    if image_query_req.thread_id is None:
        thread_id = str(uuid.uuid4())
        answer_tuple = get_combined_answer(
            image_query_req.file_id, image_query_req.query, thread_id
        )
        answer: str = answer_tuple["answer"]
        sources: list = answer_tuple["sources"]

        new_thread = CreateThread(
            thread_id=thread_id,
            external_user_id=data[TokenData.EXTERNAL_USER_ID],
            consumer_id=data[TokenData.CONSUMER_ID],
            messages=[
                get_create_message(
                    image_query_req.query,
                    answer,
                    QueryType.IMAGE.value,
                    sources,
                    file_id=image_query_req.file_id,
                )
            ],
        )

        add_new_thread(new_thread)
        thread_response = get_thread_response(
            thread_id, answer, new_thread.messages[0].sources
        )
        return thread_response
    else:
        try:
            validate_uuid(image_query_req.thread_id)
            answer_tuple = get_combined_answer(
                image_query_req.file_id,
                image_query_req.query,
                image_query_req.thread_id,
            )
            answer: str = answer_tuple["answer"]
            sources: list = answer_tuple["sources"]

            db_thread: Thread = get_thread_by_thread_id(image_query_req.thread_id)
            message = get_create_message(
                image_query_req.query,
                answer,
                QueryType.IMAGE.value,
                sources,
                db_thread.id,
                file_id=image_query_req.file_id,
            )

            add_new_message_to_thread(message)
            thread_response = get_thread_response(
                image_query_req.thread_id, answer, message.sources
            )
            return thread_response
        except InvalidUuidError as e:
            error_message = e.args[0]
            logger.error(error_message)

            raise raise_error(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=errors.INVALID_THREAD_ID,
            )


def get_combined_answer(img_query: ImageQueryRequest, thread_id: str):
    image_base64 = get_image_base64(img_query.file_id)
    vision_answer = get_openai_vision_answer(image_base64)

    template_query = messages.QUESTION_TEMPLATE.format(
        query=img_query.query, context=vision_answer
    )

    result = get_openai_answer(template_query, thread_id)
    answer: str = result["answer"]
    sources: list = result["source_documents"]

    return {"answer": answer, "sources": sources}


def get_chat_history_ser(chat_request: ChatHistoryRequest):
    thread = get_thread_by_thread_id(chat_request.thread_id)
    return thread
