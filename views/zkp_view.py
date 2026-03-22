import streamlit as st
from modules.ecc_tool import run_ecc_visualizer
from modules.modular_math import run_modular_math

def render_zkp_tab():
    # Primary Protocol Selection
    zkp_protocol = st.radio(
        label="P", 
        options=["Groth16", "Plonk", "Spartan", "Nova"], 
        key="zkp_p", 
        horizontal=True, 
        label_visibility="collapsed"
    )
    st.divider()

    if zkp_protocol == "Groth16":
        zkp_module = st.radio(
            label="M", 
            options=["Modular Arithmetic", "Extension Field", "ECC", "Weil Pairing", "Lagrange Interpolation"], 
            key="g16_m", 
            horizontal=True, 
            label_visibility="collapsed"
        )
        st.divider()
        
        if zkp_module == "Modular Arithmetic":
            run_modular_math()
        elif zkp_module == "ECC":
            ecc_sub = st.radio(
                label="E", 
                options=["Visualizer over R", "Addition over R", "Multiplication over R", "Visualizer over Fp", "Addition over Fp", "Multiplication over Fp"], 
                key="ecc_s", 
                horizontal=True, 
                label_visibility="collapsed"
            )
            st.divider()
            
            if ecc_sub == "Visualizer over R":
                run_ecc_visualizer()
            else:
                st.info(f"{ecc_sub} logic is coming soon.")
        else:
            st.info(f"{zkp_module} for Groth16 is under development.")

    elif zkp_protocol == "Plonk":
        plonk_sub = st.radio(
            label="PL", 
            options=["Tate Pairing", "KZG Commitment Scheme"], 
            key="plonk_s", 
            horizontal=True, 
            label_visibility="collapsed"
        )
        st.divider()
        st.info(f"{plonk_sub} module for Plonk is coming soon.")

    elif zkp_protocol == "Spartan":
        spartan_sub = st.radio(
            label="SP", 
            options=["Spartan Protocol", "Multilinear Extension"], 
            key="spartan_s", 
            horizontal=True, 
            label_visibility="collapsed"
        )
        st.divider()
        st.info(f"{spartan_sub} module for Spartan is coming soon.")

    elif zkp_protocol == "Nova":
        # Fixed NameError by removing undefined variable Nova_sub
        st.info("Nova protocol module is coming soon.")
