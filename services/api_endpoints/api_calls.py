import json
import re
import logging
import pandas as pd
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def generate_conversation_chat(prompt_input, session_id):
    try:
        headers = {
            'accept': 'application/json',
            'X-CSRFToken': 'OrJ1S6ddplBQrTbrcfxIOUfRE0oSixyFGNU9ImNtrebb4xhjGlljX1irLphml5fI',
        }
        params = {
            'input_message': prompt_input,
            'session_id': session_id,
        }
        response = requests.get('https://ocotopus.azurewebsites.net/chat_convo/', params=params, headers=headers)
        response.raise_for_status()
        logging.info(f'Conversation chat request succeeded: {response.status_code}')
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f'Error in generate_conversation_chat: {e}')
        return None


def generate_pdf_chat(question, session_id, file_name, follow_up=False):
    try:
        logging.info(f'Generating PDF chat for {file_name} with session_id {session_id}')
        headers = {
            'accept': 'application/json',
            'X-CSRFToken': 'OrJ1S6ddplBQrTbrcfxIOUfRE0oSixyFGNU9ImNtrebb4xhjGlljX1irLphml5fI',
        }

        params = {
            'question': question,
            'session_id': session_id,
            'file_name': file_name,
            'follow_up': follow_up
        }

        response = requests.get('https://ocotopus.azurewebsites.net/chat_pdf/', params=params, headers=headers)
        response.raise_for_status()
        response_data = json.loads(response.text)

        source_documents = process_source_documents(response_data.get('source_documents'))
        process_question_list = process_questions(response_data.get('question_suggestions')) if response_data.get(
            'question_suggestions', None) else []

        logging.info(f'PDF chat generated successfully.')
        return response_data.get('result'), source_documents, process_question_list
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        logging.error(f'Error in generate_pdf_chat: {e}')
        return None, None, None


def generate_excel_chat(question, session_id, file_name):
    try:
        headers = {
            'accept': 'application/json',
            'X-CSRFToken': 'OrJ1S6ddplBQrTbrcfxIOUfRE0oSixyFGNU9ImNtrebb4xhjGlljX1irLphml5fI',
        }

        params = {
            'question': question,
            'session_id': session_id,
            'file_name': file_name,
        }

        response = requests.get('https://ocotopus.azurewebsites.net/chat_excel/', params=params, headers=headers)
        response.raise_for_status()
        response_data = response.text
        logging.info(f'Excel chat request succeeded: {response.status_code}')

        try:
            data = json.loads(response_data)
            return data.get('answer'), data.get('log')
        except json.JSONDecodeError:
            logging.warning('Could not decode the JSON response.')
            return "Can You be more specific please", "Sorry couldn't find an answer"
    except requests.exceptions.RequestException as e:
        logging.error(f'Error in generate_excel_chat: {e}')
        return None, None


def load_excel_df(file_name):
    try:
        headers = {
            'accept': 'application/json',
            'X-CSRFToken': 'd7lrds7UaL0BQSiUS2dPcFAXGKW5XHW35twz3IHacEAWtwoMm81qlMDxN9Pz0fD6',
        }

        params = {
            'file_name': file_name,
        }

        response = requests.get('https://ocotopus.azurewebsites.net/load_excels/', params=params, headers=headers)
        response.raise_for_status()

        df = pd.DataFrame(json.loads(response.text))
        logging.info(f'Excel file {file_name} loaded successfully.')
        return df
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        logging.error(f'Error in load_excel_df: {e}')
        return pd.DataFrame()


def load_file_names():
    try:
        headers = {
            'accept': 'application/json',
            'X-CSRFToken': 'OrJ1S6ddplBQrTbrcfxIOUfRE0oSixyFGNU9ImNtrebb4xhjGlljX1irLphml5fI',
        }

        response = requests.get('https://ocotopus.azurewebsites.net/file_detials/', headers=headers)
        response.raise_for_status()

        response_data = json.loads(response.text)
        logging.info('File names loaded successfully.')
        return [entry["file_name"] for entry in response_data]
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        logging.error(f'Error in load_file_names: {e}')
        return []


def upload_files():
    try:
        headers = {
            'accept': 'application/json',
            'X-CSRFToken': 'OrJ1S6ddplBQrTbrcfxIOUfRE0oSixyFGNU9ImNtrebb4xhjGlljX1irLphml5fI',
        }

        files = {
            'file': open('FORM 18 - DON RANASINGHE DULIKA LAVANYA.pdf;type=application/pdf', 'rb'),
            'session_id': (None, 'as'),
            'access_level_id': (None, 'as'),
        }

        response = requests.post('https://ocotopus.azurewebsites.net/file_uploader/', headers=headers, files=files)
        response.raise_for_status()
        logging.info('File uploaded successfully.')
        return response.text
    except (requests.exceptions.RequestException, FileNotFoundError) as e:
        logging.error(f'Error in upload_files: {e}')
        return None


def delete_files():
    try:
        headers = {
            'accept': 'application/json',
            'X-CSRFToken': 'rbIwEMR0YzrIkFbUVoE1rH93qGMn3y4njaQyAPSEgoeswtKiTIAH9P3mTCAkprBo',
        }

        requests.get('http://127.0.0.1:8000/delete_files/', headers=headers)
        logging.info('Files deleted successfully.')
    except requests.exceptions.RequestException as e:
        logging.error(f'Error in delete_files: {e}')


def process_source_documents(data):
    try:
        data_set = []
        for page in data:
            source = {}
            source['page_content'] = page[0][1]
            source['file_name'] = page[1][1]['source']
            data_set.append(source)
        logging.info('Source documents processed successfully.')
        return data_set
    except Exception as e:
        logging.error(f'Error in process_source_documents: {e}')
        return []


def process_questions(data):
    try:
        logging.info('Processing questions.')
        lines = data.split("\n")
        lines = [line.strip() for line in lines if line.strip() != ""]

        # Extract the questions from the list
        questions = []
        for line in lines:
            if re.match(r"^\d+\.\s", line):
                questions.append(line[3:])  # Remove the numbering from the question
            elif questions:
                questions[-1] += " " + line  # Append continuation lines to the last question

        logging.info('Questions processed successfully.')
        return questions
    except Exception as e:
        logging.error(f'Error in process_questions: {e}')
        return []
