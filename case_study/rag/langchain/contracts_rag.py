from case_study.llms.ollama import get_chat
from case_study.rag.langchain.vector_store import VectorStore
from langchain_core.messages import HumanMessage

# Prompt
RAG_PROMPT = """You are a lawyer specializing in Lease Contract Renewals. Using the IRAC methodology, \
    develop legal arguments by applying the rules to the issue:\
        The issue is stated below:\
            {ISSUE} 

The relevant rules:\
{RULES}

Related clauses in other countries in the same region or country:
{CONTRACTS}

Return the output in JSON format where there are two keys, the first is the 'relevant_contracts' where the retrieved documents will reside and the second key 'explanation'. \
    Argue legally and concisely how the relevant contracts should be considered for how the rules should be applied to the facts.
"""

RETRIEVAL_PROMPT = """In the context of legal analysis of lease contract renewals, given the issue: {ISSUE} and relevant rules: {RULES}\
    Generate the best search phrase by doing the following steps:
    1. Extract the key information from the given issue
    2. Extract the relevant key words from the rules
    3. Put both together and create a query phrase to find similar clauses in the Lease Contracts Database
    The response should be in JSON format with a key 'search_phrase' 
"""


def find_application(question, relevant_rules, country, vector_store: VectorStore):
    llm, llm_json_mode = get_chat()
    query_response = llm_json_mode.invoke(
        [
            HumanMessage(
                content=RETRIEVAL_PROMPT.format(ISSUE=question, RULES=relevant_rules)
            )
        ]
    )
    search_phrase = query_response.content

    retrieved_relevant_contracts = vector_store.retriever.invoke(
        search_phrase, filter={"country": country}
    )

    # Prepare the context and prompt, and generate an answer with the LLM
    retrieved_rules_formatted = _format_docs(retrieved_relevant_contracts)
    rag_prompt_formatted = RAG_PROMPT.format(
        RULES=retrieved_rules_formatted,
        ISSUE=question,
        CONTRACTS=retrieved_rules_formatted,
    )
    answer = llm_json_mode.invoke([HumanMessage(content=rag_prompt_formatted)])
    return answer.content


def _format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
