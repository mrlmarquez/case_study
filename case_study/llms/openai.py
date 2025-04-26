from langchain_openai import ChatOpenAI


def get_chat():
    client = ChatOpenAI(model="o4-mini", temperature=0.0)
    return client
