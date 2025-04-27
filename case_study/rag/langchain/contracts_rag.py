import json
from typing import List
from case_study.llms.openai import get_chat
from case_study.models import ApplicationStep, RuleStep
from case_study.rag.langchain.vector_store import VectorStore
from langchain_core.messages import HumanMessage

# Prompt
RAG_PROMPT = """You are a lawyer specializing in Lease Contract Renewals. Using the IRAC methodology, \
    Apply the identified rule(s) to the specific facts of the scenario. Analyze how the rule(s) relate to the facts and explain the reasoning behind the application step-by-step:\
        The issue is stated below:\
            {ISSUE} 

The relevant rules:\
{RULES}

Similar clauses in other contracts in the same region or country:
{CONTRACTS}

Return the output in JSON format with a key 'explanation' which contains your application analysis.
"""

RETRIEVAL_PROMPT = """In the context of legal analysis of lease contract renewals, given the issue: {ISSUE} and relevant rules: {RULES}\
    Provide a search question aimed at finding the baseline value for the issue given the rules. 
    The response should be in JSON format with a key 'search_phrase' 
"""


def find_application(issue, relevant_rules, country, vector_store: VectorStore):
    llm_json_mode = get_chat()

    retrieved_rules_formatted = _format_rules(relevant_rules)
    query_response = llm_json_mode.invoke(
        [
            HumanMessage(
                content=RETRIEVAL_PROMPT.format(
                    ISSUE=issue, RULES=retrieved_rules_formatted
                )
            )
        ]
    )
    search_phrase = json.loads(query_response.content)["search_phrase"]

    retrieved_relevant_contracts = vector_store.retriever.invoke(
        search_phrase, filter={"country": country}
    )

    # Prepare the context and prompt, and generate an answer with the LLM
    retrieved_relevant_contracts_formatted = _format_docs(retrieved_relevant_contracts)
    rag_prompt_formatted = RAG_PROMPT.format(
        RULES=retrieved_rules_formatted,
        ISSUE=issue,
        CONTRACTS=retrieved_relevant_contracts_formatted,
    )

    answer = llm_json_mode.invoke([HumanMessage(content=rag_prompt_formatted)])
    explanation = json.loads(answer.content)["explanation"]

    application_step = ApplicationStep(
        related_clauses=[doc.page_content for doc in retrieved_relevant_contracts],
        application_explanation=explanation,
    )
    return application_step


def _format_rules(rules: List[RuleStep]):
    return "\n---\n".join(str(rule) for rule in rules)


def _format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
