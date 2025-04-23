from case_study.llms.ollama import get_chat
from case_study.rag.langchain.vector_store import VectorStore
from langchain_core.messages import HumanMessage

# Prompt
RAG_PROMPT = """You are a legal assistant who specializes in finding applicable rules given certain issues. 

The issue is stated below:

{ISSUE} 

Think carefully about the above issue. 

Now, review the following candidate rules and choose the most relevant rule(s):

{RULES}

Answer:"""


def find_applicable_rules(question, vector_store: VectorStore):
    retrieved_rules = vector_store.retriever.invoke(question)

    llm, _ = get_chat()
    # Prepare the context and prompt, and generate an answer with the LLM
    retrieved_rules_formatted = _format_docs(retrieved_rules)
    rag_prompt_formatted = RAG_PROMPT.format(
        RULES=retrieved_rules_formatted, ISSUE=question
    )
    answer = llm.invoke([HumanMessage(content=rag_prompt_formatted)])
    return answer.content


def _format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
