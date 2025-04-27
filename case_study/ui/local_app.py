from langchain_core.messages import AIMessage, HumanMessage
import streamlit as st
import asyncio

from case_study.rag.langchain.loader import load_contracts, load_rules
from case_study.ui.astream_events_handler import (
    invoke_our_graph,
)  # Utility function to handle events from astream_events from graph

# print("loading rules")
# load_rules()
# print("loading contracts")
# load_contracts()

st.title("LexiBlox Agent")
st.subheader("Review lease contracts with AI")

# Session state management for expander and graph resume after interrupt
if "expander_open" not in st.session_state:
    st.session_state.expander_open = True  # Initially keep expander open

if "graph_resume" not in st.session_state:
    st.session_state.graph_resume = (
        False  # Track if the graph should resume from a previous state
    )

# Initialize chat messages in session state
if "messages" not in st.session_state:
    # Set an initial message from the "Ai" to prompt the user
    st.session_state["messages"] = [
        AIMessage(content="Copy & paste the above example JSON in the chat")
    ]

prompt = st.chat_input()

if prompt is not None:
    st.session_state.expander_open = False  # Close expander when user enters a prompt

with st.expander(
    label="Example Input Clauses", expanded=st.session_state.expander_open
):
    """
    ```json
    {
        "active_clause": "DURATION OF TERM: A. The Primary Term and duration of the Lease shall be for a period of 5 years, commencing the 1st day of April, 2006 (the 'Commencement Date'). B.Provided the TENANT has not defaulted under the terms of this Lease, the TENANT shall have the right, privilege and option of extending this Lease for an additional period of 5 years (hereinafter referred to as Secondary Term) commencing upon the termination date of the Primary Term set forth above.The TENANT shall exercise its option for the Secondary Term ofthis Lease by delivering written notice to the LANDLORD at least 180 days prior to, and no more than 210 days prior to, the expiration of the Primary Term by Certified Mail.",
        "incoming_clause": "DURATION OF TERM: A.The Primary Term and duration of the Lease shall be for a period of 15 years, commencing the 1st day of April, 2011(the 'Commencement Date'). B.Provided the TENANT has not defaulted under the terms of this Lease, the TENANT shall have the right, privilegeand option of extending this Lease for an additional period of 15 years (hereinafter referred to as Secondary Term) commencing upon the termination date of the Primary Term set forth above.The TENANT shall exercise its option for the Secondary Term of this Lease by delivering written notice to the LANDLORD at least 180 days prior to, and no more than 210 days prior to, the expiration of the Primary Term by Certified Mail.", 
        "country": "Germany",    
        "max_retries": 3
    }
    """
# st.code(
#     """{
#         "active_clause": "DURATION OF TERM: \nA. The Primary Term and duration of the Lease shall be for a period of 5 years, commencing the 1st day of April, 2006 (the 'Commencement Date'). \nB.Provided the TENANT has not defaulted under the terms of this Lease, the TENANT shall have the right, privilege and option of extending this Lease for an additional period of 5 years (hereinafter referred to as Secondary Term) commencing upon the termination date of the Primary Term set forth above.The TENANT shall exercise its option for the Secondary Term ofthis Lease by delivering written notice to the LANDLORD at least 180 days prior to, and no more than 210 days prior to, the expiration of the Primary Term by Certified Mail.",
#         "incoming_clause": "DURATION OF TERM: \nA.The Primary Term and duration of the Lease shall be for a period of 15 years, commencing the 1st day of April, 2011(the 'Commencement Date'). \nB.Provided the TENANT has not defaulted under the terms of this Lease, the TENANT shall have the right, privilegeand option of extending this Lease for an additional period of 15 years (hereinafter referred to as Secondary Term) commencing upon the termination date of the Primary Term set forth above.The TENANT shall exercise its option for the Secondary Term of this Lease by delivering written notice to the LANDLORD at least 180 days prior to, and no more than 210 days prior to, the expiration of the Primary Term by Certified Mail.",
#         "country": "Germany",
#         "max_retries": 3,
#     }"""
# )

# Loop through all messages in the session state and render them as a chat on every st.refresh mech
for msg in st.session_state.messages:
    # https://docs.streamlit.io/develop/api-reference/chat/st.chat_message
    # we store them as AIMessage and HumanMessage as its easier to send to LangGraph
    if isinstance(msg, AIMessage):
        st.chat_message("assistant").write(msg.content)
    elif isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)

# Trigger graph interaction if there's a new user input (i.e., prompt)
if prompt:
    # Append the user's message to session state and display it
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        placeholder = (
            st.container()
        )  # Placeholder for dynamically updating agents message
        shared_state = {"graph_resume": st.session_state.graph_resume}
        response = asyncio.run(invoke_our_graph(prompt, placeholder, shared_state))
        print("assistant start")
        # Handle the response from the graph
        if type(response) is dict:  # error handling
            operation = response[
                "op"
            ]  # Check the operation type (e.g., waiting for user input)
            if operation == "on_waiting_user_resp":
                st.session_state.messages.append(
                    AIMessage(response["msg"])
                )  # graph asks user for a new response
                st.write(response["msg"])
                # Set the graph to resume from pause point after receiving more input
                st.session_state.graph_resume = True
            elif operation == "on_new_graph_msg":
                st.session_state.messages.append(AIMessage(response["msg"]))
                st.write(response["msg"])  # Display response from graph
                # graph doesn't need to resume  and can be reset, we assume from graph the response is valid
                st.session_state.graph_resume = False
            else:
                st.error("Received: " + response)  # Handle unexpected operations
        else:
            st.error("Received: " + response)  # Handle invalid response types
