import os

# from .base import *

if os.environ['STREAMLIT_ENVIORONMENT'] == 'local':
    from config.local import *
elif os.environ['STREAMLIT_ENVIORONMENT'] == 'dev':
    from config.dev import *
elif os.environ['STREAMLIT_ENVIORONMENT'] == 'prd':
    from config.prd import *
else:
    err_msg = 'STREAMLIT_ENVIORONMENT env variable is wrong'