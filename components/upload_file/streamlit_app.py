import streamlit as st
import requests


def upload_file_to_server(file, session_id=None, access_level_id=None):
    headers = {
        'accept': 'application/json',
        'X-CSRFToken': 'OrJ1S6ddplBQrTbrcfxIOUfRE0oSixyFGNU9ImNtrebb4xhjGlljX1irLphml5fI',
    }

    if file.name.endswith('.xlsx'):
        mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    elif file.name.endswith('.csv'):
        mime_type = 'text/csv'
    elif file.name.endswith('.pdf'):
        mime_type = 'application/pdf'
    else:
        raise ValueError("Unsupported file type")

    print(file.name, file, mime_type)

    files = {
        'file': (file.name, file, mime_type),
        'session_id': (None, session_id),
        'access_level_id': (None, access_level_id),
    }

    response = requests.post('https://ocotopus.azurewebsites.net/file_uploader/', headers=headers, files=files)
    return response.text


def main():
    st.title("File Upload Example")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf", "xlsx", "csv"])
    # session_id = st.text_input("Enter session ID")
    # access_level_id = st.text_input("Enter access level ID")

    if st.button("Upload"):
        if uploaded_file is not None:
            with st.spinner("File Uploading..."):
                response_text = upload_file_to_server(uploaded_file)
                st.write("FILE UPLOADED SUCCESSFULLY PLEASE PROCEED TO PDF OR EXCEL CHAT")
        else:
            st.warning("Please provide all required information.")


if __name__ == "__main__":
    st.set_page_config(page_title="File Upload Example", layout="wide")
    main()
