from langchain_ollama import ChatOllama


def get_chat():
    ### LLM

    local_llm = "llama3.2:3b-instruct-fp16"
    llm = ChatOllama(model=local_llm, temperature=0)
    llm_json_mode = ChatOllama(model=local_llm, temperature=0, format="json")
    return llm, llm_json_mode
