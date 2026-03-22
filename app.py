import streamlit as st
from modules.styles import apply_styles
from modules.ecc_tool import run_ecc_visualizer
from modules.rsa_tool import run_rsa_tool

# 1. Setup Page
st.set_page_config(page_title="Clear Cypher Lab", page_icon="🛡️", layout="wide")
apply_styles()

# 2. Sidebar with YouTube Link
with st.sidebar:
    st.title("🛡️ Navigation")
    st.markdown("---")
    st.write("📺 **Watch our Tutorials:**")
    # ایجاد یک دکمه شیک برای یوتیوب با استفاده از Markdown
    st.markdown(
        """
        <a href="https://www.youtube.com/@ClearCypherLab" target="_blank">
            <img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" width="100%">
        </a>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

# 3. Main Content
st.title("🛡️ Clear Cypher Lab")
st.markdown("Welcome to the interactive cryptography and blockchain learning environment.")

tab1, tab2 = st.tabs(["🌐 Clear ZKP", "⛓️ Blockchain"])

with tab1:
    st.header("Groth16 & ECC")
    zkp_module = st.radio("Select a Module:", ["Extension Field", "ECC Visualizer"])
    
    if zkp_module == "Extension Field":
        st.subheader("Extension Field")
        st.write("Extension Fields are fundamental in ZKP pairing-based cryptography.")
        
    elif zkp_module == "ECC Visualizer":
        run_ecc_visualizer()

with tab2:
    st.header("Blockchain Infrastructure")
    blc_module = st.radio("Select a Module:", ["RSA Practical"])
    
    if blc_module == "RSA Practical":
        run_rsa_tool()
