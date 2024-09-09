import streamlit as st
from streamlit_app import session_id
from services.api_endpoints.api_calls import generate_excel_chat, load_excel_df
import time

def main():

    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if st.session_state.file_name.endswith('.xlsx') or st.session_state.file_name.endswith('.csv'):
        df = load_excel_df(st.session_state.file_name)
        st.dataframe(df, height=400)
    else:
        st.info("Please Select a CSV file or Excel file to proceed")


    # User-provided prompt
    if prompt := st.chat_input(disabled=not (True)):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                message_placeholder = st.empty()
                full_response = ""
                assistant_response, logs = generate_excel_chat(prompt, session_id, st.session_state.file_name)
                # Simulate stream of response with milliseconds delay
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.06)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

                with st.expander("Source Citation"):
                    st.markdown(
                        f'<div style="overflow-y: scroll; max-height: 300px;">{logs}</div>',
                        unsafe_allow_html=True
                    )
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
