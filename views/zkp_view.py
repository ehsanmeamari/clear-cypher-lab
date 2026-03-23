import streamlit as st
from modules.ecc_tool import run_ecc_visualizer
from modules.modular_math import modular_math
from modules.ecc_fp import ecc_fp

def render_zkp_tab():
    # Balanced CSS for a better visual layout and compact expanders
    st.markdown("""
        <style>
            /* Adjust radio button margins to prevent empty spaces */
            div[data-testid="stRadio"] { margin-top: -10px !important; margin-bottom: 10px !important; }
            
            /* Proper spacing for dividers */
            hr { margin-top: 10px !important; margin-bottom: 15px !important; opacity: 0.2; }
            
            /* Increase vertical gap for better page fill */
            [data-testid="stVerticalBlock"] > div { gap: 1rem !important; }
            
            /* Remove internal padding for all Expanders to keep them tight */
            [data-testid="stExpanderDetails"] {
                padding-top: 0px !important;
                padding-bottom: 0px !important;
            }
        </style>
        """, unsafe_allow_html=True)

    # --- 1. Primary Protocol Selection ---
    zkp_protocol = st.radio(
        label="Protocol", 
        options=["Groth16", "Plonk", "Spartan", "Nova"], 
        key="zkp_p", 
        horizontal=True, 
        label_visibility="collapsed"
    )
    st.divider()

    if zkp_protocol == "Groth16":
        # --- 2. Module Selection for Groth16 ---
        zkp_module = st.radio(
            label="Module", 
            options=["Modular Arithmetic", "Extension Field", "ECC", "Weil Pairing", "Lagrange Interpolation"], 
            key="g16_m", 
            horizontal=True, 
            label_visibility="collapsed"
        )
        st.divider()

        if zkp_module == "Modular Arithmetic":
            modular_math()

        elif zkp_module == "ECC":
            # --- 3. ECC Sub-module Selection ---
            ecc_sub = st.radio(
                label="ECC Sub", 
                options=[
                    "Visualizer over R", "Addition over R", "Multiplication over R", 
                    "Visualizer over Fp", "Finite Field Fp", "Extension Fields"
                ], 
                key="ecc_s", 
                horizontal=True, 
                label_visibility="collapsed"
            )
            st.divider()

            if ecc_sub == "Finite Field Fp":
                # Calling the main ECC function
                ecc_fp()
            elif ecc_sub == "Visualizer over R":
                run_ecc_visualizer()
            else:
                st.info(f"{ecc_sub} logic is coming soon.")
