import streamlit as st
from modules.styles import apply_styles
from modules.ecc_tool import run_ecc_visualizer
from modules.modular_math import run_modular_math

# 1. Page Configuration (No changes here)
st.set_page_config(
    page_title="Clear Cypher Lab", 
    page_icon="logo.png", 
    layout="wide"
)

apply_styles()

# 2. Header Section: Logo (Left) and Social Media (Right)
col_main, col_social = st.columns([4, 1])

with col_main:
    # --- LOGO SIZE REDUCED HERE ---
    # Width changed from 450 to 225 (half size)
    st.image("logo.png", width=225) 
    
    # Styled subtitle (No changes, but kept for context)
    st.markdown('<div style="text-align: left; padding-left: 10px; font-size: 1.1em; color: #334e68; font-weight: 500;">Interactive Cryptography Learning Environment</div>', unsafe_allow_html=True)

with col_social:
    # Social Media section (No changes here)
    st.write("🔗 **Social Media:**")
    # YouTube Button
    st.markdown(
        """<a href="https://www.youtube.com/@ClearCypherLab" target="_blank" style="text-decoration: none;">
        <div style="background-color: #FF0000; color: white; padding: 10px; text-align: center; border-radius: 5px; font-weight: bold; margin-bottom: 10px;">
        📺 YOUTUBE
        </div></a>""", 
        unsafe_allow_html=True)
    # LinkedIn Button
    st.markdown(
        """<a href="https://www.linkedin.com/company/113012501/" target="_blank" style="text-decoration: none;">
        <div style="background-color: #0077B5; color: white; padding: 10px; text-align: center; border-radius: 5px; font-weight: bold;">
        🔗 LINKEDIN
        </div></a>""", 
        unsafe_allow_html=True)

st.write("") # Spacer
st.divider()

# 3. Navigation Tabs
tab1, tab2, tab3 = st.tabs(["🌐 Cryptography", "⛓️ Blockchain", "🔐 ZKP"])

with tab1:
    st.info("🚀 Advanced modules coming soon.")

with tab2:
    st.info("🚀 Simulation tools coming soon.")

with tab3:
    # LEVEL 1: Protocol Selection
    zkp_protocol = st.radio(
        label="Select Protocol:",
        options=["Groth16", "Plonk", "Spartan"],
        key="zkp_protocol_selection",
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.divider()

    # --- LOGIC FOR GROTH16 ---
    if zkp_protocol == "Groth16":
        zkp_module = st.radio(
            label="Groth16 Modules",
            options=["Modular Arithmetic", "Extension Field", "ECC", "Weil Pairing", "Lagrange Interpolation"], 
            key="groth16_sub",
            horizontal=True,
            label_visibility="collapsed"
        )
        st.divider()
        
        if zkp_module == "Modular Arithmetic":
            run_modular_math()
            
        elif zkp_module == "ECC":
            ecc_sub_module = st.radio(
                label="ECC Operations:",
                options=["Visualizer over R", "Addition over R", "Multiplication over R", "Visualizer over Fp", "Addition over Fp", "Multiplication over Fp"],
                key="ecc_sub_selection",
                horizontal=True,
                label_visibility="collapsed"
            )
            
            st.divider()
            
            if ecc_sub_module == "Visualizer over R":
                run_ecc_visualizer()

            elif ecc_sub_module == "Addition over R":
                st.info("Point Addition logic ($P + Q = R$) over R is coming soon.")

            elif ecc_sub_module == "Multiplication over R":
                st.info("Scalar Multiplication over R is coming soon.")

            elif ecc_sub_module == "Visualizer over Fp":
                st.info("Visualizer over Fp is coming soon.")            
                
            elif ecc_sub_module == "Addition over Fp":
                st.info("Point Addition logic ($P + Q = R$) over a finite field is coming soon.")
                
            elif ecc_sub_module == "Multiplication over Fp":
                st.info("Scalar Multiplication logic ($[k]P$) using double-and-add is coming soon.")
        
        else:
            st.info(f"{zkp_module} for Groth16 is currently under development.")

    # --- LOGIC FOR PLONK ---
    elif zkp_protocol == "Plonk":
        plonk_sub = st.radio(
            label="Plonk Modules",
            options=["Tate Pairing", "KZG Commitment Scheme"],
            key="plonk_sub",
            horizontal=True,
            label_visibility="collapsed"
        )
        st.divider()
        st.info(f"{plonk_sub} module for Plonk is coming soon.")

    # --- LOGIC FOR Spartan ---
    elif zkp_protocol == "Spartan":
        Spartan_sub = st.radio(
            label="Spartan Modules",
            options=["Spartan Protocol", "Multilinear Extension"],
            key="Spartan_sub",
            horizontal=True,
            label_visibility="collapsed"
        )
        st.divider()
        st.info(f"{Spartan_sub} module for Spartan is coming soon.")

st.divider()
