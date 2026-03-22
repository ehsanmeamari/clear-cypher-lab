import streamlit as st
from modules.styles import apply_styles
from modules.ecc_tool import run_ecc_visualizer
from modules.modular_math import run_modular_math

# 1. Page Configuration
st.set_page_config(
    page_title="Clear Cypher Lab", 
    page_icon="logo.png", 
    layout="wide"
)

# ULTRA-TIGHT SPACING CSS
st.markdown("""
    <style>
        /* Remove padding from the main container */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
            max-width: 95% !important;
        }
        
        /* Eliminate space between all Streamlit elements */
        [data-testid="stVerticalBlock"] > div {
            flex-direction: column;
            gap: 0px !important;
        }

        /* Tighten Radio Buttons */
        div[data-testid="stRadio"] {
            margin-bottom: -15px !important;
        }
        
        /* Tighten Dividers */
        hr {
            margin-top: 5px !important;
            margin-bottom: 5px !important;
            border: 0;
            border-top: 1px solid #eee;
        }

        /* Adjust Image and Header alignment */
        [data-testid="stImage"] {
            margin-bottom: -10px !important;
        }

        /* Tabs padding reduction */
        button[data-baseweb="tab"] {
            padding-top: 5px !important;
            padding-bottom: 5px !important;
        }
    </style>
    """, unsafe_allow_html=True)

apply_styles()

# 2. Header Section
col_main, col_social = st.columns([5, 1])

with col_main:
    st.image("logo.png", width=200) 
    st.markdown('<div style="text-align: left; padding-left: 5px; font-size: 1.05em; color: #334e68; margin-top: -10px;">Interactive Cryptography Learning Environment</div>', unsafe_allow_html=True)

with col_social:
    st.markdown('<p style="margin-bottom: 2px; font-weight: bold; font-size: 0.85em;">🔗 Social Media:</p>', unsafe_allow_html=True)
    st.markdown(
        """<div style="display: flex; flex-direction: column; gap: 4px;">
        <a href="https://www.youtube.com/@ClearCypherLab" target="_blank" style="text-decoration: none;">
            <div style="background-color: #FF0000; color: white; padding: 4px; text-align: center; border-radius: 4px; font-weight: bold; font-size: 0.75em;">📺 YOUTUBE</div>
        </a>
        <a href="https://www.linkedin.com/company/113012501/" target="_blank" style="text-decoration: none;">
            <div style="background-color: #0077B5; color: white; padding: 4px; text-align: center; border-radius: 4px; font-weight: bold; font-size: 0.75em;">🔗 LINKEDIN</div>
        </a>
        </div>""", unsafe_allow_html=True)

st.divider()

# 3. Navigation Tabs
tab1, tab2, tab3 = st.tabs(["🌐 Cryptography", "⛓️ Blockchain", "🔐 ZKP"])

with tab1:
    st.info("🚀 Advanced modules coming soon.")

with tab2:
    st.info("🚀 Simulation tools coming soon.")

with tab3:
    # Use columns to make radios even tighter if needed
    zkp_protocol = st.radio(label="P", options=["Groth16", "Plonk", "Spartan"], key="zkp_p", horizontal=True, label_visibility="collapsed")
    st.divider()

    if zkp_protocol == "Groth16":
        zkp_module = st.radio(label="M", options=["Modular Arithmetic", "Extension Field", "ECC", "Weil Pairing", "Lagrange Interpolation"], key="g16_m", horizontal=True, label_visibility="collapsed")
        st.divider()
        
        if zkp_module == "Modular Arithmetic":
            run_modular_math()
            
        elif zkp_module == "ECC":
            ecc_sub = st.radio(label="E", options=["Visualizer over R", "Addition over R", "Multiplication over R", "Visualizer over Fp", "Addition over Fp", "Multiplication over Fp"], key="ecc_s", horizontal=True, label_visibility="collapsed")
            st.divider()
            
            if ecc_sub == "Visualizer over R":
                run_ecc_visualizer()
            else:
                st.info(f"{ecc_sub} logic is coming soon.")
        else:
            st.info(f"{zkp_module} for Groth16 is under development.")

    elif zkp_protocol == "Plonk":
        plonk_sub = st.radio(label="PL", options=["Tate Pairing", "KZG Commitment Scheme"], key="plonk_s", horizontal=True, label_visibility="collapsed")
        st.divider()
        st.info(f"{plonk_sub} module for Plonk is coming soon.")

    elif zkp_protocol == "Spartan":
        spartan_sub = st.radio(label="SP", options=["Spartan Protocol", "Multilinear Extension"], key="spartan_s", horizontal=True, label_visibility="collapsed")
        st.divider()
        st.info(f"{spartan_sub} module for Spartan is coming soon.")

st.divider()
