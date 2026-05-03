import streamlit as st
from modules.ecc_overR import run_ecc_overR
from modules.modular_math import run_modular_math
from modules.ecc_math import ecc_fp
from modules.pairing import pairing
from modules.extension_math import extension_math
# Step 1: Import updated function names from modules.lagrange
from modules.lagrange import lagrange_real_ui, lagrange_fp_ui 

def render_zkp_tab():
    # --- CSS Styling ---
    st.markdown("""
        <style>
            [data-testid="stVerticalBlock"] > div { gap: 0.1rem !important; padding-top: 0rem; }
            div[data-testid="stRadio"] { margin-top: -18px !important; margin-bottom: -12px !important; }
            hr { margin-top: 2px !important; margin-bottom: 5px !important; opacity: 0.1; }
            .main .block-container { padding-top: 0rem; }
            [data-testid="stExpanderDetails"] { padding-top: 0px !important; padding-bottom: 0px !important; }
        </style>
        """, unsafe_allow_html=True)

    # --- Protocol Selection ---
    zkp_protocol = st.radio(
        label="Protocol", options=["Groth16", "Plonk", "Spartan", "Nova"], 
        key="zkp_p", horizontal=True, label_visibility="collapsed"
    )
    st.divider()

    if zkp_protocol == "Groth16":
        zkp_module = st.radio(
            label="Module", 
            options=["Modular Arithmetic", "Extension Field", "ECC", "Weil Pairing", "Lagrange Interpolation"], 
            key="g16_m", horizontal=True, label_visibility="collapsed"
        )
        st.divider()
         
        if zkp_module == "Modular Arithmetic":
            run_modular_math()
        elif zkp_module == "Extension Field":
            extension_math()
        elif zkp_module == "ECC":
            ecc_sub = st.radio(
                label="ECC Sub", 
                options=["Over R", "Over Fp"], 
                key="ecc_s", horizontal=True, label_visibility="collapsed"
            )
            st.divider()
            if ecc_sub == "Over R":
                run_ecc_overR()
            else: 
                ecc_fp()
        elif zkp_module == "Weil Pairing":
            pairing()
            
        elif zkp_module == "Lagrange Interpolation":
            # Selection for Real vs Finite Field mode
            lagrange_mode = st.radio(
                label="Select Calculation Mode",
                options=["Real Numbers", "Finite Field (Fp)"],
                key="lag_mode", horizontal=True
            )
            st.divider()
            
            if lagrange_mode == "Real Numbers":
                lagrange_real_ui()
            else:
                lagrange_fp_ui()
