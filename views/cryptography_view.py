import streamlit as st
from modules.cryptography.aes import aes_ui

def render_cryptography_tab():
    # --- CSS Styling ---
    st.markdown("""
        <style>
            [data-testid="stVerticalBlock"] > div { gap: 0.1rem !important; padding-top: 0rem; }
            div[data-testid="stRadio"] { margin-top: -18px !important; margin-bottom: -12px !important; }
            hr { margin-top: 2px !important; margin-bottom: 5px !important; opacity: 0.1; }
            .main .block-container { padding-top: 0rem; }
            [data-testid="stExpanderDetails"] { padding-top: 0px !important; padding-bottom: 0px !important; }
        </style>
        """, unsafe_allow_html=True)

    # --- Algorithm Selection ---
    section = st.radio(
        label="Section",
        options=["AES"],
        key="crypto_section",
        horizontal=True,
        label_visibility="collapsed"
    )
    st.divider()

    if section == "AES":
        aes_ui()
