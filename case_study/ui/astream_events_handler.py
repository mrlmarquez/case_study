import json
import streamlit as st

# from graph import graph
from case_study.graphs.irac import IRACGraph
from case_study.ui.text_formatter import rules_to_list_section, to_simple_markdown

# Configuration for thread processing with a "specific" thread ID
# this is key for dynamic interrupts
# it allows the graph to remember the previous conversation
# why it stopped and to resume from that point
thread_config = {"configurable": {"thread_id": "1"}}
irac = IRACGraph()
graph = irac.graph


# Asynchronous function to process events from the graph and update Streamlit UI
async def invoke_our_graph(st_messages, st_placeholder, st_state):
    """
    Asynchronously processes a stream of events from the graph_runnable and updates the Streamlit interface.

    Args:
        st_messages (list): List of messages to be sent to the graph_runnable.
        st_placeholder (st.beta_container): Streamlit placeholder used to display updates and statuses.
        st_state (dict): State information for controlling graph resume behavior.
    """
    print("============================")
    print("invoke_our_graph start")
    container = st_placeholder
    st_input = json.loads(st_messages)

    # If the graph has been previously interrupted
    # we have to resume from that point by
    # updating the graph state instead of sending new input
    if st_state.get("graph_resume"):
        graph.update_state(
            thread_config, {"input": st_messages}
        )  # Update the graph's state with the new input
        st_input = None  # No new input is passed if resuming the graph

    # invoke the graph as normal but depending on if the input is `None` or a `str` the graph will resume
    async for event in graph.astream_events(st_input, thread_config, version="v2"):
        name = event["name"]

        # if name == "on_issue_identified":
        #     with container:
        #         state = event["data"]["input"]

        #     return {
        #         "op": "on_new_graph_msg",
        #         "msg": to_simple_markdown("Issue", state["issue"]),
        #     }

        # if name == "on_rules_retrieved":
        #     with container:
        #         state = event["data"]["input"]

        #     return {
        #         "op": "on_new_graph_msg",
        #         "msg": rules_to_list_section(
        #             "Applicable Internal Rules", state["rule_step"]
        #         ),
        #     }

        # if name == "on_application":
        #     with container:
        #         state = event["data"]["input"]

        #     return {
        #         "op": "on_new_graph_msg",
        #         "msg": to_simple_markdown(
        #             "Applying the Rule(s)",
        #             state["application_step"]["application_explanation"],
        #         ),
        #     }

        # if name == "on_conclusion":
        #     with container:
        #         st.balloons()
        #         state = event["data"]["input"]

        #     return {
        #         "op": "on_new_graph_msg",
        #         "msg": to_simple_markdown(
        #             "Conclusion",
        #             state["application_step"]["conclusion"],
        #         ),
        #     }

        # the graph issued an interrupt that the user needs to update/handle
        if name == "on_waiting_user_resp":
            # Display the issue/error and prompt the user for a new response or update
            container.error(
                "The length of the word is " + str(event["data"]) + " letters long"
            )

        if name == "on_complete_graph":
            with container:
                st.balloons()
                state = event["data"]["input"]
                issue = to_simple_markdown("Issue", state["issue"])
                rules = rules_to_list_section(
                    "Applicable Internal Rules", state["rule_step"]
                )
                application = to_simple_markdown(
                    "Applying the Rule(s)",
                    state["application_step"].application_explanation,
                )
                conclusion = to_simple_markdown(
                    "Conclusion",
                    state["conclusion"],
                )
                output = f"{issue}\n\n {rules}\n\n {application} \n\n {conclusion}"
            # Return success message with processed data
            return {
                "op": "on_new_graph_msg",
                "msg": f"{output} \n:fairy:",
            }

    # Retrieve the current state of the graph to check for any pending tasks or interruptions
    state = graph.get_state(thread_config)

    # If there are any pending tasks and interruptions, handle them
    if len(state.tasks) != 0 and len(state.next) != 0:
        issue = (
            state.tasks[0].interrupts[0].value
        )  # Retrieve the first interrupt value from the task
        # Return an operation indicating the graph is waiting for the user to respond
        return {"op": "on_waiting_user_resp", "msg": issue}
