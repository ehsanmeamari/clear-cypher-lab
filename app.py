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

# Custom CSS for better logo and text alignment
st.markdown("""
    <style>
        .block-container { 
            padding-top: 0.5rem !important; 
            padding-bottom: 0rem !important; 
        }
        [data-testid="stVerticalBlock"] > div { gap: 0rem !important; }
        
        /* Logo and text styling */
        [data-testid="stImage"] { 
            display: flex; 
            justify-content: center; 
            margin-bottom: 8px !important;
        }
        .logo-text {
            text-align: center; 
            font-size: 1.35em; 
            font-weight: 700; 
            color: #1e3a8a; 
            margin-top: 0px !important;
            letter-spacing: 1px;
        }
    </style>
    """, unsafe_allow_html=True)

apply_styles()

# 2. Header Section
col_left, col_center, col_right = st.columns([1, 3, 1])

with col_left:
    st.empty()

with col_center:
    # Display the logo
    st.image("logo.png", width=220)
    
    # Logo text directly below the image
    st.markdown('<div class="logo-text">CLEAR CYPHER LAB</div>', unsafe_allow_html=True)

    # Subtitle
    st.markdown('''
        <div style="text-align: center; font-size: 1.05em; color: #334e68; 
                    margin-top: 12px; font-weight: 500;">
            Interactive Cryptography Learning Environment
        </div>
    ''', unsafe_allow_html=True)

with col_right:
    # Social Media Section
    st.markdown('<div style="text-align: right;">', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 5px; font-weight: bold; font-size: 0.8em; color: #555;">🔗 Social Media</p>', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="display: flex; flex-direction: column; gap: 4px; align-items: flex-end;">
            <a href="https://www.youtube.com/@ClearCypherLab" target="_blank" style="text-decoration: none;">
                <div style="background-color: #FF0000; color: white; padding: 4px 12px; text-align: center; border-radius: 4px; font-weight: bold; font-size: 0.7em; min-width: 90px;">📺 YOUTUBE</div>
            </a>
            <a href="https://www.linkedin.com/company/113012501/" target="_blank" style="text-decoration: none;">
                <div style="background-color: #0077B5; color: white; padding: 4px 12px; text-align: center; border-radius: 4px; font-weight: bold; font-size: 0.7em; min-width: 90px;">🔗 LINKEDIN</div>
            </a>
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
