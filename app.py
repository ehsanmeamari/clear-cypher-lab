import streamlit as st
from modules.styles import apply_styles
from views.header_view import render_header_view  # فراخوانی هدر جدید
from views.cryptography_view import render_cryptography_tab
from views.blockchain_view import render_blockchain_tab
from views.zkp_view import render_zkp_tab

# 1. Page Configuration
st.set_page_config(
    page_title="Clear Cypher Lab", 
    page_icon="logo.png", 
    layout="wide"
)

# ULTRA-COMPACT CSS - Centralized layout adjustments
st.markdown("""
    <style>
        .block-container { padding-top: 2.5rem !important; padding-bottom: 0rem !important; }
        [data-testid="stVerticalBlock"] > div { gap: 0rem !important; }
        div[data-testid="stRadio"] { margin-bottom: -25px !important; }
        hr { margin-top: 2px !important; margin-bottom: 2px !important; }
        button[data-baseweb="tab"] { padding-top: 0px !important; padding-bottom: 0px !important; height: 35px !important; }
    </style>
    """, unsafe_allow_html=True)

apply_styles()

# 2. Render Header (Moved to separate view file)
render_header_view()

# 3. Navigation Tabs
tab1, tab2, tab3 = st.tabs(["🌐 Cryptography", "⛓️ Blockchain", "🔐 ZKP"])

with tab1: render_cryptography_tab()
with tab2: render_blockchain_tab()
with tab3: render_zkp_tab()

st.divider()
