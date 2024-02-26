import uuid
from datetime import datetime

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import S3FileLoader

from src.apis.v1.enums.attribute_info import AttributeInfo
from src.core.config.settings import settings
from src.core.db.repositories.log import add_log
from src.core.db.repositories.vector import get_vectorization_files
from src.core.db.repositories.vector import update_file_status
from src.core.langchain.openai import get_chat_suggestions_openai
from src.core.langchain.openai_config import get_openai_embedding
from src.core.utils.error_messages import errors
from src.core.vector_db.chroma_db import get_chroma_client
from src.core.vector_db.chroma_db import get_vector_db


def queue_status_ser():
    return get_vectorization_files()


def vectorization_ser():
    vector_files = get_vectorization_files()

    if len(vector_files) == 0:
        return errors.NO_FILES_TO_VECTORIZED

    print("Start Time", str(datetime.now()))

    client = get_chroma_client()
    embeddings = get_openai_embedding()
    collection = client.get_or_create_collection(name=settings.VECTOR_DB_COLL_NAME)

    doc_collections = []
    for file in vector_files:
        fileName = settings.AWS_FOLDER_NAME + "/" + file.name
        loader = S3FileLoader(
            settings.AWS_BUCKET_NAME,
            fileName,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_ACCESS_KEY_SECRET,
            region_name=settings.AWS_REGION_NAME,
        )

        doc = loader.load()

        chunk_size = settings.TEXT_SPLIT_CHUNK_SIZE
        chunk_overlap = settings.TEXT_SPLIT_CHUNK_OVERLAP
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        doc_splits = text_splitter.split_documents(doc)
        print("Document Name =>", file.name)
        print("Collection Started", str(datetime.now()))

        doc_contents: list[str] = []
        doc_metadatas: list[object] = []
        doc_embeddings = []
        doc_ids: list[str] = []

        for doc in doc_splits:
            doc_content = doc.page_content
            doc_contents.append(doc_content)

            guid_id = uuid.uuid4()
            doc_id = str(guid_id)
            doc_ids.append(doc_id)

            doc_metadata = doc.metadata
            doc_metadata[AttributeInfo.ID.value] = file.id
            doc_metadata[AttributeInfo.NAME.value] = file.name
            doc_metadata[AttributeInfo.FILE_PATH.value] = file.file_path
            doc_metadata[AttributeInfo.UUID.value] = doc_id
            doc_metadata[AttributeInfo.DB_CREATED_ON.value] = str(file.created_on)
            doc_metadata[AttributeInfo.VECTORIZED_ON.value] = str(datetime.now())
            doc_metadatas.append(doc_metadata)

            doc_embedding = embeddings.embed_query(doc_content)
            doc_embeddings.append(doc_embedding)

        collection.add(
            documents=doc_contents,
            metadatas=doc_metadatas,
            embeddings=doc_embeddings,
            ids=doc_ids,
        )
        doc_collections.append(
            {
                "documents": doc_contents,
                "metadatas": doc_metadatas,
                "ids": doc_ids,
            }
        )
        print(collection.count())
        print("Collection Ended", str(datetime.now()))

        update_file_status(file.id)

    print("End Time", str(datetime.now()))

    return {"vector_files": vector_files, "doc_collections": doc_collections}


def query_vector_ser(query: str):
    try:
        add_log("persist_directory", "info")
        vectordb = get_vector_db()
        result1 = vectordb.similarity_search(query)
        add_log("vector db start", "info")
        retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 2})
        result2 = retriever.get_relevant_documents(query)

        return {"result1": result1, "result2": result2}
    except Exception as error:
        add_log(str(error), "error")
        raise error


def query_openai_llm_ser(query: str):
    try:
        result = get_chat_suggestions_openai(query)
        return result
    except Exception as error:
        add_log(str(error), "error")
        raise error
