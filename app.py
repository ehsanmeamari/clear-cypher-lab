import streamlit as st
from modules.styles import apply_styles
from modules.ecc_tool import run_ecc_visualizer

# Setup Page
st.set_page_config(page_title="Clear Cypher Lab", page_icon="🛡️", layout="wide")
apply_styles()

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
    st.info("RSA Module is coming to the next update!")

st.divider()
st.caption("Clear Cypher Lab © 2026")
