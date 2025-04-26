import json
from langgraph.graph import StateGraph, END

from case_study.llms.ollama import get_chat
from case_study.models import GraphState

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.callbacks import adispatch_custom_event
from case_study.rag.langchain.contracts_rag import find_application
from case_study.rag.langchain.rules_rag import find_applicable_rules
from case_study.rag.langchain.vector_store import VectorStore

IDENTIFY_ISSUE_INSTRUCTIONS = "You are a seasoned lawyer specializing in Lease Contracts dealings.\
    You are to analyze what is the issue when comparing the given active clause and the proposed renewal clause.\
    Provide a concise analysis with reasonable basis.\
    Return JSON with two keys, the key 'issue' is the concise description of the issue. The key 'basis' is the concise explanation of why it is an issue and indicate the statement(s) where the issue is found."


IDENTIFY_ISSUE_PROMPT = (
    "The active clause in the current contract: {ACTIVE_CLAUSE}\n\n \
        The renewal clause in the proposed new contract: {INCOMING_CLAUSE}"
)
CONCLUSION_INSTRUCTION = (
    "You are a seasoned lawyer specializing in Lease Contracts dealings. Using the IRAC methodology, \
    based on the application of the rule(s) to the issue, what is the most likely conclusion or outcome of the legal issue? \
    Provide a clear and concise conclusion. Mention elements in the issue as necessary."
)
CONCLUSION_PROMPT = "Provide the conclusion given the following inputs:\n \
        ISSUE: {ISSUE}\n\n \
        RULE(S): {RULES}\n\n \
        APPLICATION: {APPLICATION}\n\n \
    Return a JSON with a key 'conclusion' and put your conclusion in there."

rules_store = VectorStore(doc_type="rules")
contracts_store = VectorStore(doc_type="contracts")


# NODES
async def identify_issue(state: GraphState):
    active_clause = state["active_clause"]
    proposed_clause = state["incoming_clause"]

    _, llm_json_mode = get_chat()
    identify_issue_prompt_formatted = IDENTIFY_ISSUE_PROMPT.format(
        ACTIVE_CLAUSE=active_clause, INCOMING_CLAUSE=proposed_clause
    )
    result = llm_json_mode.invoke(
        [
            SystemMessage(content=IDENTIFY_ISSUE_INSTRUCTIONS),
            HumanMessage(content=identify_issue_prompt_formatted),
        ]
    )
    content = json.loads(result.content)
    print(content)
    result = content["basis"]
    state["issue"] = result
    return state


async def retrieve_rule(state: GraphState):
    issue = state["issue"]
    retrieved_rules = find_applicable_rules(issue, rules_store)
    state["rule_step"] = retrieved_rules
    return state


async def apply(state: GraphState):
    issue = state["issue"]
    relevant_rules = state["rule_step"]
    country = state["country"]

    application_step = find_application(
        issue=issue,
        relevant_rules=relevant_rules,
        country=country,
        vector_store=contracts_store,
    )

    state["application_step"] = application_step
    return state


async def conclude(state: GraphState):
    issue = state["issue"]
    rules_formatted = "\n".join([str(rule) for rule in state["rule_step"]])
    application_formatted = str(state["application_step"])

    _, llm_json_mode = get_chat()
    conclusion_prompt_formatted = CONCLUSION_PROMPT.format(
        ISSUE=issue, RULES=rules_formatted, APPLICATION=application_formatted
    )
    result = llm_json_mode.invoke(
        [
            SystemMessage(content=CONCLUSION_INSTRUCTION),
            HumanMessage(content=conclusion_prompt_formatted),
        ]
    )
    conclusion = json.loads(result.content)
    print(conclusion)
    state["conclusion"] = conclusion["conclusion"]
    return state


# EDGE
async def did_we_arrive_to_a_conclusion(state: GraphState):
    await adispatch_custom_event(
        "on_complete_graph", {"input": state, "len": len(state)}
    )
    return "yes"


class IRACGraph:
    def __init__(self):
        self.workflow = StateGraph(GraphState)
        self.workflow.add_node("identify_issue", identify_issue)
        self.workflow.add_node("retrieve_rule", retrieve_rule)
        self.workflow.add_node("apply", apply)
        self.workflow.add_node("conclude", conclude)

        self.workflow.add_edge("identify_issue", "retrieve_rule")
        self.workflow.add_edge("retrieve_rule", "apply")
        self.workflow.add_edge("apply", "conclude")
        self.workflow.add_conditional_edges(
            "conclude",
            did_we_arrive_to_a_conclusion,
            {"no": "identify_issue", "yes": END},
        )
        self.workflow.set_entry_point("identify_issue")
        self.graph = self.workflow.compile()

    def stream(self, inputs, stream_mode):
        return self.graph.stream(inputs, stream_mode)
