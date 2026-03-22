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

# Custom CSS to reduce vertical spacing
st.markdown("""
    <style>
        /* Reduce spacing between elements globally */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 0rem;
        }
        /* Tighten radio button spacing */
        div[data-testid="stRadio"] > div {
            gap: 5px;
        }
        /* Reduce space around dividers */
        hr {
            margin-top: 10px !important;
            margin-bottom: 10px !important;
        }
        /* Reduce space around info boxes */
        .stAlert {
            margin-top: -10px;
        }
    </style>
    """, unsafe_allow_html=True)

apply_styles()

# 2. Header Section
col_main, col_social = st.columns([4, 1])

with col_main:
    st.image("logo.png", width=225) 
    st.markdown('<div style="text-align: left; padding-left: 10px; font-size: 1.1em; color: #334e68; font-weight: 500; margin-top: -15px;">Interactive Cryptography Learning Environment</div>', unsafe_allow_html=True)

with col_social:
    st.write("🔗 **Social Media:**")
    st.markdown(
        """<a href="https://www.youtube.com/@ClearCypherLab" target="_blank" style="text-decoration: none;">
        <div style="background-color: #FF0000; color: white; padding: 5px; text-align: center; border-radius: 5px; font-weight: bold; margin-bottom: 5px; font-size: 0.8em;">
        📺 YOUTUBE
        </div></a>""", unsafe_allow_html=True)
    st.markdown(
        """<a href="https://www.linkedin.com/company/113012501/" target="_blank" style="text-decoration: none;">
        <div style="background-color: #0077B5; color: white; padding: 5px; text-align: center; border-radius: 5px; font-weight: bold; font-size: 0.8em;">
        🔗 LINKEDIN
        </div></a>""", unsafe_allow_html=True)

st.divider()

# 3. Navigation Tabs
tab1, tab2, tab3 = st.tabs(["🌐 Cryptography", "⛓️ Blockchain", "🔐 ZKP"])

with tab1:
    st.info("🚀 Advanced modules coming soon.")

with tab2:
    st.info("🚀 Simulation tools coming soon.")

with tab3:
    # LEVEL 1
    zkp_protocol = st.radio(label="P", options=["Groth16", "Plonk", "Spartan"], key="zkp_p", horizontal=True, label_visibility="collapsed")
    st.divider()

    if zkp_protocol == "Groth16":
        # LEVEL 2
        zkp_module = st.radio(label="M", options=["Modular Arithmetic", "Extension Field", "ECC", "Weil Pairing", "Lagrange Interpolation"], key="g16_m", horizontal=True, label_visibility="collapsed")
        st.divider()
        
        if zkp_module == "Modular Arithmetic":
            run_modular_math()
            
        elif zkp_module == "ECC":
            # LEVEL 3
            ecc_sub = st.radio(label="E", options=["Visualizer over R", "Addition over R", "Multiplication over R", "Visualizer over Fp", "Addition over Fp", "Multiplication over Fp"], key="ecc_s", horizontal=True, label_visibility="collapsed")
            st.divider()
            
            if ecc_sub == "Visualizer over R":
                run_ecc_visualizer()
            elif ecc_sub == "Addition over R":
                st.info("Point Addition logic ($P + Q = R$) over R is coming soon.")
            elif ecc_sub == "Multiplication over R":
                st.info("Scalar Multiplication over R is coming soon.")
            elif ecc_sub == "Visualizer over Fp":
                st.info("Visualizer over Fp is coming soon.")            
            elif ecc_sub == "Addition over Fp":
                st.info("Point Addition logic ($P + Q = R$) over a finite field is coming soon.")
            elif ecc_sub == "Multiplication over Fp":
                st.info("Scalar Multiplication logic ($[k]P$) using double-and-add is coming soon.")
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
