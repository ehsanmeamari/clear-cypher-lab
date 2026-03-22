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

# 2. Header Section - Fixed Final Version
# Using 2 columns instead of 3 to prevent right-side clipping
col_main, col_social = st.columns([4, 1])

with col_main:
    # Centering the logo and text manually using margin-left
    st.markdown(
        """
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-left: 20%;">
            <img src="https://raw.githubusercontent.com/ehsanmeamari/clear-cypher-lab/main/logo.png" width="160">
            <div style="font-size: 1.1em; color: #334e68; margin-top: 10px; font-weight: 500; text-align: center;">
                Interactive Cybersecurity Learning Environment
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )

with col_social:
    # Forced alignment to the absolute right with no room for error
    st.markdown("""
        <div style="text-align: right; width: 100%; display: flex; flex-direction: column; align-items: flex-end;">
            <p style="font-weight: bold; font-size: 0.85em; color: #555; margin-bottom: 8px; margin-top: 0px;">
                🔗 Social Media
            </p>
            <div style="display: flex; flex-direction: column; gap: 5px;">
                <a href="https://www.youtube.com/@ClearCypherLab" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #FF0000; color: white; padding: 5px 12px; border-radius: 4px; font-weight: bold; font-size: 0.75em; width: 95px; text-align: center;">
                        📺 YOUTUBE
                    </div>
                </a>
                <a href="https://www.linkedin.com/company/113012501/" target="_blank" style="text-decoration: none;">
                    <div style="background-color: #0077B5; color: white; padding: 5px 12px; border-radius: 4px; font-weight: bold; font-size: 0.75em; width: 95px; text-align: center;">
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
