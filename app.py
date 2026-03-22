import streamlit as st
from modules.styles import apply_styles
# Import functions from views
from views.cryptography_view import render_cryptography_tab
from views.blockchain_view import render_blockchain_tab
from views.zkp_view import render_zkp_tab

# 1. Page Configuration
st.set_page_config(
    page_title="Clear Cypher Lab", 
    page_icon="logo.png", 
    layout="wide"
)

# ULTRA-COMPACT CSS
st.markdown("""
    <style>
        .block-container { padding-top: 0.5rem !important; padding-bottom: 0rem !important; }
        [data-testid="stVerticalBlock"] > div { gap: 0rem !important; }
        div[data-testid="stRadio"] { margin-bottom: -25px !important; }
        hr { margin-top: 2px !important; margin-bottom: 2px !important; }
        [data-testid="stImage"] { margin-bottom: -20px !important; }
        button[data-baseweb="tab"] { padding-top: 0px !important; padding-bottom: 0px !important; height: 35px !important; }
        .stMarkdown div p { margin-bottom: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

apply_styles()

# 2. Header Section
col_main, col_social = st.columns([5, 1])

with col_main:
    st.image("logo.png", width=180) 
    st.markdown('<div style="text-align: left; padding-left: 5px; font-size: 1em; color: #334e68; margin-top: 10px; font-weight: 500;">Interactive Cryptography Learning Environment</div>', unsafe_allow_html=True)

with col_social:
    st.markdown('<p style="margin-top: 5px; margin-bottom: 2px; font-weight: bold; font-size: 0.8em;">🔗 Social Media:</p>', unsafe_allow_html=True)
    st.markdown(
        """<div style="display: flex; flex-direction: column; gap: 2px;">
        <a href="https://www.youtube.com/@ClearCypherLab" target="_blank" style="text-decoration: none;">
            <div style="background-color: #FF0000; color: white; padding: 2px 8px; text-align: center; border-radius: 4px; font-weight: bold; font-size: 0.7em;">📺 YOUTUBE</div>
        </a>
        <a href="https://www.linkedin.com/company/113012501/" target="_blank" style="text-decoration: none;">
            <div style="background-color: #0077B5; color: white; padding: 2px 8px; text-align: center; border-radius: 4px; font-weight: bold; font-size: 0.7em;">🔗 LINKEDIN</div>
        </a>
        </div>""", unsafe_allow_html=True)

st.divider()

# 3. Navigation Tabs
tab1, tab2, tab3 = st.tabs(["🌐 Cryptography", "⛓️ Blockchain", "🔐 ZKP"])

with tab1:
    render_cryptography_tab()

with tab2:
    render_blockchain_tab()

with tab3:
    render_zkp_tab()

st.divider()
