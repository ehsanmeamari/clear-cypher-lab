import streamlit as st

st.set_page_config(page_title="Clear Cypher Lab", page_icon="🛡️", layout="wide")

# Corrected CSS: Added 2rem to top padding
st.markdown("""
    <style>
           .block-container {
                padding-top: 2rem; 
                padding-bottom: 0rem;
                padding-left: 5rem;
                padding-right: 5rem;
            }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Clear Cypher Lab")
st.markdown("Welcome to the interactive cryptography and blockchain learning environment.")

tab1, tab2 = st.tabs(["🌐 Clear ZKP", "⛓️ Blockchain"])

with tab1:
    st.header("Groth16")
    zkp_module = st.radio("Select a Module:", ["Extension Field", "ECC Visualizer"])
    
    if zkp_module == "Extension Field":
        st.subheader("Groth16 Protocol")
        st.write("Groth16 is one of the most efficient zk-SNARK constructions.")
        
    elif zkp_module == "ECC Visualizer":
        st.subheader("Elliptic Curve Cryptography")
        st.latex(r"y^2 = x^3 + ax + b")

with tab2:
    st.header("Blockchain Infrastructure")
    blc_module = st.radio("Select a Module:", ["RSA Practical"])
    
    if blc_module == "RSA Practical":
        st.subheader("RSA Encryption Demo")
        message = st.text_input("Enter message:", "Hello")
        if message:
            # Simplified ASCII shift for visual demo
            st.success(f"Encrypted Result: {'-'.join([hex(ord(c)) for c in message])}")

st.divider()
st.caption("Clear Cypher Lab © 2026")
