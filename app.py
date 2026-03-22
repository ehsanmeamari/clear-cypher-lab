import streamlit as st
from modules.styles import apply_styles
from modules.ecc_tool import run_ecc_visualizer
from modules.modular_math import run_modular_math

# 1. Page Configuration
st.set_page_config(page_title="Clear Cypher Lab", page_icon="🛡️", layout="wide")
apply_styles()

# 2. RTL (Right-to-Left) Support CSS
st.markdown(
    """
    <style>
    .main, div[data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }
    div[data-testid="stMarkdownContainer"] p {
        text-align: right;
    }
    div.row-widget.stRadio > div {
        flex-direction: row-reverse;
        justify-content: flex-end;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
st.markdown("Interactive Cryptography Learning Environment")

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
        options=["Groth16", "Plonk", "Sumcheck"],
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
            run_ecc_visualizer()
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

    # --- LOGIC FOR SUMCHECK ---
    elif zkp_protocol == "Sumcheck":
        # LEVEL 2: Sumcheck Sub-modules
        sumcheck_sub = st.radio(
            label="Sumcheck Modules",
            options=["SumCheck Protocol", "Multilinear Extension"],
            key="sumcheck_sub",
            horizontal=True,
            label_visibility="collapsed"
        )
        st.divider()
        st.info(f"{sumcheck_sub} module for Sumcheck is coming soon.")

st.divider()
