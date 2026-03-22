import streamlit as st
from modules.styles import apply_styles
from modules.ecc_tool import run_ecc_visualizer

# Page Configuration
st.set_page_config(page_title="Clear Cypher Lab", page_icon="🛡️", layout="wide")
apply_styles()

# Sidebar Navigation & Social Media Links
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

# Main Header
st.title("🛡️ Clear Cypher Lab")
st.markdown("Interactive Cryptography Learning Environment")

# Defining Tabs
tab1, tab2, tab3 = st.tabs(["🌐 Cryptography", "⛓️ Blockchain", "🔐 ZKP"])

with tab1:
    st.header("Cryptography")
    st.info("Advanced cryptography modules are under development.")
    st.write("Upcoming: RSA, AES, and Digital Signatures.")

with tab2:
    st.header("Blockchain Infrastructure")
    st.info("Blockchain simulation tools coming soon.")
    st.write("Upcoming: Merkle Trees and Consensus Algorithms.")

with tab3:
    st.header("Groth 16")
    
    # ZKP Roadmap Selection
    zkp_module = st.radio(
        "Select a Module:", 
        ["Modular Arithmetic", "Extension Field", "ECC", "Weil Pairing", "Lagrange Interpolation"], 
        key="zkp_main",
        horizontal=True
    )
    
    st.divider()

    if zkp_module == "Modular Arithmetic":
        st.subheader("Modular Arithmetic")
        st.write("Fundamental math for finite fields.")
        # Simple Calculator
        num_a = st.number_input("Enter a:", value=17)
        num_n = st.number_input("Enter mod n:", value=5)
        st.code(f"{num_a} mod {num_n} = {num_a % num_n}", language="text")

    elif zkp_module == "Extension Field":
        st.subheader("Extension Field")
        st.info("Pairing-friendly field operations coming soon.")
        
    elif zkp_module == "ECC":
        ecc_sub = st.selectbox("ECC Operations:", ["Visualizer", "Point Addition", "Scalar Multiplication"])
        if ecc_sub == "Visualizer":
            run_ecc_visualizer()
        else:
            st.info(f"{ecc_sub} tool is under development.")

    elif zkp_module == "Weil Pairing":
        st.subheader("Weil Pairing")
        st.info("Bilinear pairings roadmap.")

    elif zkp_module == "Lagrange Interpolation":
        st.subheader("Lagrange Interpolation")
        st.info("Polynomial interpolation for ZK-STARKs.")

st.divider()
