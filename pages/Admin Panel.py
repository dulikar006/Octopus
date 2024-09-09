import streamlit as st
import streamlit_shadcn_ui as ui

st.subheader("Upload Knowledge")

ui.tabs(options=['HR Expert', 'Finance Expert', 'Marketing Expert', 'Expertee'], default_value='Overview', key="main_tabs")
