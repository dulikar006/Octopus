import streamlit_shadcn_ui as ui
import streamlit as st
import requests
import time

from clients.openai_client import call_openai
import uuid

session_id = str(uuid.uuid4())

cols = st.columns(3)
with cols[0]:
    ui.card(title="Total Revenue", content="$45,231.89", description="+20.1% from last month", key="card1").render()
with cols[1]:
    ui.card(title="Subscriptions", content="+2350", description="+180.1% from last month", key="card2").render()
with cols[2]:
    ui.card(title="Sales", content="+12,234", description="+19% from last month", key="card3").render()

st.subheader("Chat With Expert")

# Use the selected tab to track which expert the user is interacting with
tab = ui.tabs(options=['HR Expert', 'Finance Expert', 'Marketing Expert', 'Expertee'], default_value='Overview',
              key="main_tabs")


# Function for generating LLM response
def generate_response(expert, prompt_input, session_id):
    return call_openai('You are an {expert} please answer below questions, {input}',
                       {"input": prompt_input, "expert": expert})


# Generator for bot response
def bot_resp(expert, question):
    assistant_response = generate_response(expert, question, session_id)
    for char in assistant_response:
        yield char
        time.sleep(0.005)


# Main chat UI function
def chat_ui(expert_key, expert_name):
    # Create unique key for each expert's chat history
    if f"{expert_key}_messages" not in st.session_state:
        st.session_state[f"{expert_key}_messages"] = [
            {"role": "assistant", "content": f"I'm {expert_name}. How may I help you?"}]

    # Display chat messages
    for message in st.session_state[f"{expert_key}_messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided prompt
    if prompt := st.chat_input(disabled=not (True)):
        st.session_state[f"{expert_key}_messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if the last message is not from the assistant
    if st.session_state[f"{expert_key}_messages"][-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                bot_response = bot_resp(expert_name, prompt)
            response = st.write_stream(bot_response)

        # Add assistant response to chat history
        st.session_state[f"{expert_key}_messages"].append({"role": "assistant", "content": response})


# Handling chat UI for each tab with unique session state key
if tab == 'HR Expert':
    chat_ui("hr_expert", "HR Expert")

elif tab == 'Finance Expert':
    chat_ui("finance_expert", "Finance Expert")

elif tab == 'Marketing Expert':
    chat_ui("marketing_expert", "Marketing Expert")

elif tab == 'Expertee':
    chat_ui("expertee", "Expert In All HR, Finance, Marketing")
