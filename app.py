import streamlit as st
from modules.styles import apply_styles
from modules.ecc_tool import run_ecc_visualizer
from modules.modular_math import run_modular_math  # Import the new module

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

# 4. Main Content Header
st.title("🛡️ Clear Cypher Lab")
st.markdown("Interactive Cryptography Learning Environment")

# Defining Tabs
tab1, tab2, tab3 = st.tabs(["🌐 Cryptography", "⛓️ Blockchain", "🔐 ZKP"])

with tab1:
    st.header("Cryptography")
    st.info("🚀 Advanced cryptography modules are under development.")

with tab2:
    st.header("Blockchain Infrastructure")
    st.info("🚀 Blockchain simulation tools coming soon.")

with tab3:
    st.header("Groth 16")
    
    # Main ZKP Navigation (Label Hidden)
    zkp_module = st.radio(
        label="Select a Module:",
        options=["Modular Arithmetic", "Extension Field", "ECC", "Weil Pairing", "Lagrange Interpolation"], 
        key="zkp_main",
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.divider()

    # Module Logic
    if zkp_module == "Modular Arithmetic":
        run_modular_math()  # Using the imported function
        
    elif zkp_module == "Extension Field":
        st.subheader("Extension Field")
        st.info("Field extension operations (Fp^k) coming soon.")
        
    elif zkp_module == "ECC":
        st.subheader("Elliptic Curve Cryptography")
        ecc_sub = st.selectbox("ECC Operations:", ["Visualizer", "Point Addition", "Scalar Multiplication"])
        if ecc_sub == "Visualizer":
            run_ecc_visualizer()
        else:
            st.info(f"{ecc_sub} tool is under development.")

    elif zkp_module == "Weil Pairing":
        st.subheader("Weil Pairing")
        st.info("Bilinear pairings and Miller's algorithm coming soon.")

    elif zkp_module == "Lagrange Interpolation":
        st.subheader("Lagrange Interpolation")
        st.info("Polynomial interpolation for ZK-proofs coming soon.")

st.divider()
