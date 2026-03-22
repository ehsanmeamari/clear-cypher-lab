import streamlit as st
from modules.styles import apply_styles
from modules.ecc_tool import run_ecc_visualizer
from modules.modular_math import run_modular_math

# 1. Page Configuration (Icon changed to your new logo file)
st.set_page_config(
    page_title="Clear Cypher Lab", 
    page_icon="logo.png", 
    layout="wide"
)

apply_styles()

# 2. Sidebar Logo
# Make sure "logo.png" is in the same directory as this file
try:
    st.sidebar.image("logo.png", use_container_width=True)
except Exception:
    st.sidebar.warning("Logo file not found. Check filename.")

st.sidebar.markdown("---")

# 3. Sidebar Navigation
with st.sidebar:
    st.title("🛡️ Clear Cypher Lab")
    st.markdown("---")
    st.write("🔗 **Social Media:**")
    
    col_yt, col_li = st.columns(2)
    with col_yt:
        st.markdown(
            """<a href="https://www.youtube.com/@ClearCypherLab" target="_blank">
            <img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" width="100%"></a>""", 
            unsafe_allow_html=True)
    with col_li:
        st.markdown(
            """<a href="https://www.linkedin.com/company/113012501/" target="_blank">
            <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" width="100%"></a>""", 
            unsafe_allow_html=True)
    st.markdown("---")

# 4. Main Header
st.title("🛡️ Clear Cypher Lab")
# We use a div to force this specific line to the left
st.markdown('<div style="text-align: left;">Interactive Cryptography Learning Environment</div>', unsafe_allow_html=True)

# 5. Top-Level Tabs
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
        # LEVEL 2: Groth16 Sub-modules
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
            # New sub-menu for ECC
            ecc_sub_module = st.radio(
                label="ECC Operations:",
                options=["Visualizer over R", "Addition over R", "Multiplication over R", "Visualizer over Fp", "Addition over Fp", "Multiplication over Fp"],
                key="ecc_sub_selection",
                horizontal=True,
                label_visibility="collapsed"
            )
            
            st.divider()
            
            if ecc_sub_module == "Visualizer over R":
                run_ecc_visualizer() # Your existing function

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
        # LEVEL 2: Plonk Sub-modules
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
        # LEVEL 2: Spartan Sub-modules
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
