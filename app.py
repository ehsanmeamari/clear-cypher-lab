import streamlit as st
from modules.styles import apply_styles
from modules.ecc_tool import run_ecc_visualizer
from modules.rsa_tool import run_rsa_tool

# Page Setup
st.set_page_config(page_title="Clear Cypher Lab", page_icon="🛡️", layout="wide")
apply_styles()

# Sidebar Navigation
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

# Main Content
st.title("🛡️ Clear Cypher Lab")
st.markdown("Welcome to the interactive cryptography learning environment.")

tab1, tab2 = st.tabs(["🌐 Clear ZKP", "⛓️ Blockchain"])

with tab1:
    st.header("Groth16 & ECC")
    
    # First level: Main Module Selection
    zkp_module = st.radio("Select a Module:", ["Extension Field", "ECC"], key="zkp_main")
    
    if zkp_module == "Extension Field":
        st.subheader("Extension Field")
        st.write("Extension Fields are fundamental in ZKP pairing-based cryptography.")
        
    elif zkp_module == "ECC":
        st.markdown("---")
        # Second level: ECC Sub-modules
        ecc_sub_module = st.selectbox(
            "ECC Operations:", 
            ["Visualizer", "Point Addition", "Scalar Multiplication"]
        )
        
        if ecc_sub_module == "Visualizer":
            run_ecc_visualizer()
        elif ecc_sub_module == "Point Addition":
            st.subheader("ECC Point Addition")
            st.info("Interactive Point Addition (P + Q) - Module under development.")
        elif ecc_sub_module == "Scalar Multiplication":
            st.subheader("ECC Scalar Multiplication")
            st.info("Scalar Multiplication (nP) - Module under development.")

with tab2:
    st.header("Blockchain Infrastructure")
    blc_module = st.radio("Select a Module:", ["RSA Practical"], key="blc")
    if blc_module == "RSA Practical":
        run_rsa_tool()

st.divider()
