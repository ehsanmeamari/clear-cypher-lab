import streamlit as st
from modules.styles import apply_styles
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
        [data-testid="stImage"] { margin-bottom: -20px !important; display: flex; justify-content: center; }
        button[data-baseweb="tab"] { padding-top: 0px !important; padding-bottom: 0px !important; height: 35px !important; }
        .stMarkdown div p { margin-bottom: 0px !important; }
        
        /* Center alignment for the whole header block */
        .centered-header {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)

apply_styles()

# 2. Header Section (Centered)
st.markdown('<div class="centered-header">', unsafe_allow_html=True)

# Logo
col_img_1, col_img_2, col_img_3 = st.columns([1, 1, 1])
with col_img_2:
    st.image("logo.png", width=180) 

# Subtitle
st.markdown('<div style="font-size: 1.1em; color: #334e68; margin-top: 15px; font-weight: 500;">Interactive Cryptography Learning Environment</div>', unsafe_allow_html=True)

# Social Media Buttons (Horizontal)
st.markdown("""
    <div style="display: flex; flex-direction: column; align-items: center; margin-top: 15px; gap: 8px;">
        <p style="margin-bottom: 5px; font-weight: bold; font-size: 0.9em; color: #555;">🔗 Social Media</p>
        <div style="display: flex; flex-direction: row; gap: 15px; justify-content: center;">
            <a href="https://www.youtube.com/@ClearCypherLab" target="_blank" style="text-decoration: none;">
                <div style="background-color: #FF0000; color: white; padding: 6px 20px; text-align: center; border-radius: 4px; font-weight: bold; font-size: 0.8em; min-width: 110px;">📺 YOUTUBE</div>
            </a>
            <a href="https://www.linkedin.com/company/113012501/" target="_blank" style="text-decoration: none;">
                <div style="background-color: #0077B5; color: white; padding: 6px 20px; text-align: center; border-radius: 4px; font-weight: bold; font-size: 0.8em; min-width: 110px;">🔗 LINKEDIN</div>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

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
