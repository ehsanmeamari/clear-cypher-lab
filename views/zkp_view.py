import streamlit as st
from modules.ecc_tool import run_ecc_visualizer
from modules.modular_math import run_modular_math
from modules.ecc_math import ecc_fp

def render_zkp_tab():
    # Optimized CSS to remove extra white spaces and compress elements
    st.markdown("""
        <style>
            /* 1. Reduce gap between all Streamlit vertical blocks */
            [data-testid="stVerticalBlock"] > div { gap: 0.1rem !important; padding-top: 0rem; }
            
            /* 2. Remove radio button margins to align with dividers */
            div[data-testid="stRadio"] { margin-top: -18px !important; margin-bottom: -12px !important; }
            
            /* 3. Minimize thickness and spacing of dividers */
            hr { margin-top: 2px !important; margin-bottom: 5px !important; opacity: 0.1; }

            /* 4. Remove top page padding */
            .main .block-container { padding-top: 0rem; }

            /* 5. Remove internal padding from Expanders for a compact look */
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
            run_modular_math()
            
        elif zkp_module == "Extension Field":
            extension_math()
        
        elif zkp_module == "ECC":
            # --- 3. ECC Sub-module Selection ---
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
                run_ecc_visualizer()
            elif ecc_sub in ["Addition over Fp", "Multiplication over Fp", "Visualizer over Fp"]:
                # Calling the ECC Fp logic
                ecc_fp()
            else:
                st.info(f"{ecc_sub} logic is coming soon.")

        elif zkp_module == "Weil Pairing":

        elif zkp_module == "Lagrange Interpolation":
            st.info("Lagrange Interpolation logic is coming soon.")
