class Messages:
    BEARER = "bearer"
    QUESTION_TEMPLATE = """For this query {query}. Analyze the provided context
    {context} thoroughly to grasp the subject matter and question,
    prioritize factual accuracy in responses based on the latest knowledge,
    structure the response logically to ensure coherence and flow,
    employ clear and precise language to convey information effectively,
    integrate relevant knowledge to enhance responses,
    and consider providing credible sources if necessary
    to support the information provided"""

    SYSTEM_MESSAGE_TEMPLATE = r"""Given a specific context, please give a short answer to the question,
    covering the required advices in general and then provide the names
    all of relevant(even if it relates a bit) products.
    ----
    {context}
    Chat History: {chat_history}
    ----
    """

    USER_MESSAGE_TEMPLATE = "Question:```{question}```"


messages = Messages()
