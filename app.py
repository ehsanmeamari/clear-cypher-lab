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
        [data-testid="stImage"] { display: flex; justify-content: center; margin-bottom: -15px !important; }
        button[data-baseweb="tab"] { padding-top: 0px !important; padding-bottom: 0px !important; height: 35px !important; }
        .stMarkdown div p { margin-bottom: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

apply_styles()

# 2. Header Section
col_left, col_center, col_right = st.columns([1, 1, 1])

with col_left:
    st.empty() 

with col_center:
    # Absolute centering for Logo and Subtitle
    st.markdown(
        """
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <img src="https://raw.githubusercontent.com/ehsanmeamari/clear-cypher-lab/main/logo.png" width="160">
            <div style="font-size: 1.1em; color: #334e68; margin-top: 15px; font-weight: 500; text-align: center;">
                Interactive Cybersecurity Learning Environment
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )

with col_right:
    # Creating a single container for all right-side elements
    st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: flex-end; width: 100%;">
            <div style="font-weight: bold; font-size: 0.8em; color: #555; margin-bottom: 8px; text-align: right;">
                🔗 Social Media
            </div>
            <div style="display: flex; flex-direction: column; gap: 5px;">
                <a href="https://www.youtube.com/@ClearCypherLab" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #FF0000; color: white; padding: 5px 12px; border-radius: 4px; font-weight: bold; font-size: 0.75em; width: 100px; text-align: center;">
                        📺 YOUTUBE
                    </div>
                </a>
                <a href="https://www.linkedin.com/company/113012501/" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #0077B5; color: white; padding: 5px 12px; border-radius: 4px; font-weight: bold; font-size: 0.75em; width: 100px; text-align: center;">
                        🔗 LINKEDIN
                    </div>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
