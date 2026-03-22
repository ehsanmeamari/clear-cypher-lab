import streamlit as st
from modules.styles import apply_styles
from modules.ecc_tool import run_ecc_visualizer
from modules.rsa_tool import run_rsa_tool

# Page Configuration
st.set_page_config(page_title="Clear Cypher Lab", page_icon="🛡️", layout="wide")
apply_styles()

# Sidebar Navigation & Social Media
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
    zkp_module = st.radio("Select a Module:", ["Extension Field", "ECC Visualizer"], key="zkp")
    if zkp_module == "ECC Visualizer":
        run_ecc_visualizer()
    else:
        st.write("Extension Fields coming soon...")

with tab2:
    st.header("Blockchain Infrastructure")
    blc_module = st.radio("Select a Module:", ["RSA Practical"], key="blc")
    if blc_module == "RSA Practical":
        run_rsa_tool()
