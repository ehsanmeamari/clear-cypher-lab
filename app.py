# --- فایل app.py ---
import streamlit as st
from modules.styles import apply_styles
from views.header_view import render_header_view
from views.cryptography_view import render_cryptography_tab
from views.blockchain_view import render_blockchain_tab
from views.zkp_view import render_zkp_tab

st.set_page_config(
    page_title="Clear Cypher Lab", 
    page_icon="logo.png", 
    layout="wide"
)

# حذف کامل هدر سیستم و کاهش پدینگ محتوا به صفر
st.markdown("""
    <style>
        /* مخفی کردن هدر پیش‌فرض استریم‌لیت */
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* حذف فضای خالی بالای صفحه */
        .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
        [data-testid="stVerticalBlock"] > div { gap: 0rem !important; }
        div[data-testid="stRadio"] { margin-bottom: -25px !important; }
        hr { margin-top: 2px !important; margin-bottom: 2px !important; }
    </style>
    """, unsafe_allow_html=True)

apply_styles()
render_header_view()

tab1, tab2, tab3 = st.tabs(["🌐 Cryptography", "⛓️ Blockchain", "🔐 ZKP"])
with tab1: render_cryptography_tab()
with tab2: render_blockchain_tab()
with tab3: render_zkp_tab()
