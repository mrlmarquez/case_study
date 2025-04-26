from langchain_openai import ChatOpenAI


def get_chat():
    client = ChatOpenAI(model="o4-mini")
    json_llm = client.bind(response_format={"type": "json_object"})
    return json_llm
