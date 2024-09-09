import streamlit as st
import requests
from Home import session_id
import time

from clients.openai_client import call_openai


def main():

    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


    # Function for generating LLM response
    def generate_response(prompt_input, session_id):


        # headers = {
        #     'accept': 'application/json',
        #     'X-CSRFToken': 'OrJ1S6ddplBQrTbrcfxIOUfRE0oSixyFGNU9ImNtrebb4xhjGlljX1irLphml5fI',
        # }
        # params = {
        #     'input_message': prompt_input,
        #     'session_id': session_id,
        # }
        # response = requests.get('https://ocotopus.azurewebsites.net/chat_convo/', params=params, headers=headers)
        # print(response.text)
        # return response.text

        call_openai(prompt_input)


    # User-provided prompt
    if prompt := st.chat_input(disabled=not (True)):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        # with st.chat_message("assistant"):
        #     with st.spinner("Thinking..."):
        #         response = generate_response(prompt, session_id)
        #         st.write(response)
        # message = {"role": "assistant", "content": response}
        # st.session_state.messages.append(message)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                message_placeholder = st.empty()
                full_response = ""
                assistant_response = generate_response(prompt, session_id)
                # Simulate stream of response with milliseconds delay
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.06)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
