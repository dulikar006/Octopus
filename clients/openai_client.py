import logging
import os

import streamlit as st
from langchain_openai import AzureChatOpenAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from config import llm_model

logger = logging.getLogger(__name__)


def call_openai(base_prompt, input):
    try:

        # llm = AzureChatOpenAI(
        #     api_key=os.environ.get('llm_api_key'),
        #     api_version=llm_model.get('api_version'),
        #     azure_endpoint=llm_model.get('azure_endpoint'),
        #     model=llm_model.get('model')
        # )

        llm = AzureChatOpenAI(
            api_key='9cae1c98f81247a7a02c8e0b3c2bee76',
            api_version='2024-02-15-preview',
            azure_endpoint="https://mcap-eus-mts-ark-openai.openai.azure.com/openai/deployments/GPT_4o/chat/completions?api-version=2024-02-15-preview",
            model='GPT_4o'
        )

        prompt = PromptTemplate(
            input_variables=list(input.keys()),
            template=base_prompt)

        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        result = chain.invoke(input)

        # log = {'input': input, 'output': result}
        # json_handler = JSONHandler('llm_log.json', st.session_state.buy_state)
        # json_handler.update_json(log)

        return result
    except Exception as err:
        st.error(f'Error Calling Open AI API, Try again later - Error: {err}')
        logger.error(f'Error Calling Open AI API - Error: {err}')
