import json
from case_study.llms.ollama import get_chat
from case_study.models import RuleStep
from case_study.rag.langchain.vector_store import VectorStore
from langchain_core.messages import HumanMessage

# Prompt
RULES_RETRIEVAL_FORMAT = (
    "What is the relevant rule(s) that applies to the issue identified below? {ISSUE}"
)
RAG_PROMPT = """Using the IRAC Analysis, provide a brief explanation of the rule(s) and any relevant case law or statutory provisions.

The rule:

{RULES}

The response should be in JSON format with a key 'explanation' which contains the explanation of the rule(s)."""


def find_applicable_rules(issue, vector_store: VectorStore):
    retrieved_rules = vector_store.retriever.invoke(
        RULES_RETRIEVAL_FORMAT.format(ISSUE=issue)
    )
    rules_result = []
    for rule in retrieved_rules:
        _, llm = get_chat()
        # Prepare the context and prompt, and generate an answer with the LLM
        retrieved_rules_formatted = _format_docs([rule])
        rag_prompt_formatted = RAG_PROMPT.format(
            RULES=retrieved_rules_formatted, ISSUE=issue
        )

        response = llm.invoke([HumanMessage(content=rag_prompt_formatted)])
        response_json = json.loads(response.content)
        rule_step = RuleStep(
            rule=rule.page_content, explanation=response_json["explanation"]
        )
        rules_result.append(rule_step)
    return rules_result


def _format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
