import streamlit as st
from modules.cryptography.aes import aes_ui

def render_cryptography_tab():
    section = st.segmented_control(
        "Section",
        options=["AES"],
        default=None,
        key="crypto_section",
        label_visibility="collapsed"
    )
    if section == "AES":
        aes_ui()
