import streamlit as st
from Home import session_id
from services.api_endpoints.api_calls import generate_pdf_chat
import time


def main():
    followup = st.radio("Generate Follow-up Questions:", ["YES", "NO"])
    if followup == "YES":
        follow_up = True
    else:
        follow_up = False

    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided prompt
    if prompt := st.chat_input(disabled=not (True)):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if the last message is not from the assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                message_placeholder = st.empty()
                full_response = ""
                assistant_response, source_data_list, f_q = generate_pdf_chat(prompt, session_id,
                                                                              st.session_state.file_name, follow_up)

                # Simulate stream of response with milliseconds delay
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.06)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

                # Combine content from all items in the list
                combined_content = "\n\n".join(item['page_content'] for item in source_data_list)

                # Create a single expander with the combined content
                with st.expander("Source Citation"):
                    st.markdown(
                        f'<div style="overflow-y: scroll; max-height: 300px;">{combined_content}</div>',
                        unsafe_allow_html=True
                    )

                if f_q is not None:
                    with st.expander("Follow-up Question"):
                        for item in f_q:
                            st.write(f"- {item}")

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
