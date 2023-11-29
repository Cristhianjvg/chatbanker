from pdfminer.high_level import extract_text
import os
import tempfile
import streamlit as st
from .Agent import Agent


def is_openai_api_key_set() -> bool:
    return len(st.session_state["OPENAI_API_KEY"]) > 0

def read_and_save_file(Agent, files):
    # st.file_uploader(
    #     "Upload document",
    #     type=["pdf"],
    #     key="file_uploader",
    #     on_change=read_and_save_file,
    #     label_visibility="collapsed",
    #     accept_multiple_files=True,
    #     disabled=not is_openai_api_key_set(),
    # )
    return None


# Uso de la función
ruta_del_archivo = 'static/crucero.pdf'  # Reemplaza esto con la ruta a tu archivo PDF
ruta_del_txt = 'static/chatbot.txt'  # Reemplaza esto con la ruta a tu archivo txt
# read_and_save_file(ruta_del_archivo, ruta_del_txt)
