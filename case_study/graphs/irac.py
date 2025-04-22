import json
from langgraph.graph import StateGraph, END

from case_study.llms.ollama import get_chat
from case_study.models import GraphState

from langchain_core.messages import HumanMessage, SystemMessage

IDENTIFY_ISSUE_INSTRUCTIONS = "You are a seasoned lawyer specializing in Lease Contracts dealings.\
    You are to analyze what is the issue when comparing the given active clause and the proposed renewal clause.\
    Provide a concise analysis with reasonable basis.\
    Return JSON with two keys, the key 'issue' is the concise description of the issue. The key 'basis' is the concise explanation of why it is an issue."


IDENTIFY_ISSUE_PROMPT = (
    "The active clause in the current contract: {ACTIVE_CLAUSE}\n\n \
        The renewal clause in the proposed new contract: {INCOMING_CLAUSE}"
)


# NODES
def identify_issue(state: GraphState):
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
    result = content["issue"]
    state["issue"] = result
    return state


def retrieve_rule(state: GraphState):
    return "retrieve_rule"


def retrieve_historical_application(state: GraphState):
    return "retrieve_historical_application"


def conclude(state: GraphState):
    return "conclude"


# EDGE
def did_we_arrive_to_a_conclusion(state: GraphState):
    return END


class IRACGraph:
    def __init__(self):
        self.workflow = StateGraph(GraphState)
        self.workflow.add_node("identify_issue", identify_issue)
        self.workflow.add_node("retrieve_rule", retrieve_rule)
        self.workflow.add_node(
            "retrieve_historical_application", retrieve_historical_application
        )
        self.workflow.add_node("conclude", conclude)

        self.workflow.add_edge("identify_issue", "retrieve_rule")
        self.workflow.add_edge("retrieve_rule", "retrieve_historical_application")
        self.workflow.add_edge("retrieve_historical_application", "conclude")
        self.workflow.add_conditional_edges(
            "conclude",
            did_we_arrive_to_a_conclusion,
            {"no": "identify_issue", "yes": END},
        )
        self.workflow.set_entry_point("identify_issue")
        self.graph = self.workflow.compile()

    def stream(self, inputs, stream_mode):
        return self.graph.stream(inputs, stream_mode)
