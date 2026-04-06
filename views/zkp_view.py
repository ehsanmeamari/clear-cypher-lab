import streamlit as st
from modules.ecc_overR import run_ecc_overR
from modules.modular_math import run_modular_math
from modules.ecc_math import ecc_fp
from modules.pairing import pairing
from modules.extension_math import extension_math
# Step 1: Import your new module here (Create a file named number_systems.py in modules)
# from modules.number_systems import run_number_systems 

def render_zkp_tab():
    # CSS remains the same to keep the UI compact
    st.markdown("""
        <style>
            [data-testid="stVerticalBlock"] > div { gap: 0.1rem !important; padding-top: 0rem; }
            div[data-testid="stRadio"] { margin-top: -18px !important; margin-bottom: -12px !important; }
            hr { margin-top: 2px !important; margin-bottom: 5px !important; opacity: 0.1; }
            .main .block-container { padding-top: 0rem; }
            [data-testid="stExpanderDetails"] { padding-top: 0px !important; padding-bottom: 0px !important; }
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
        # Added "Number Systems" as the first step for Digital Literacy
        zkp_module = st.radio(
            label="Module", 
            options=["Modular Arithmetic", "Extension Field", "ECC", "Weil Pairing", "Lagrange Interpolation"], 
            key="g16_m", 
            horizontal=True, 
            label_visibility="collapsed"
        )
        st.divider()
         
        if zkp_module == "Modular Arithmetic":
            run_modular_math()
            
        elif zkp_module == "Extension Field":
            extension_math()
        
        elif zkp_module == "ECC":
            ecc_sub = st.radio(
                label="ECC Sub", 
                options=[
                    "Visualizer over R", "Addition over R", "Multiplication over R", 
                    "Visualizer over Fp", "Addition over Fp", "Multiplication over Fp"
                ], 
                key="ecc_s", 
                horizontal=True, 
                label_visibility="collapsed"
            )
            st.divider()
            
            if ecc_sub == "Visualizer over R":
                run_ecc_overR()
            elif ecc_sub in ["Addition over Fp", "Multiplication over Fp", "Visualizer over Fp"]:
                ecc_fp()
            else:
                st.info(f"{ecc_sub} logic is coming soon.")

        elif zkp_module == "Weil Pairing":
            # Using the improved pairing() function we just fixed
            pairing()
            
        elif zkp_module == "Lagrange Interpolation":
            st.info("Lagrange Interpolation logic is coming soon.")
