import streamlit as st

st.set_page_config(page_title="Clear Cypher Lab", page_icon="🛡️", layout="wide")

# CSS to inject for removing top padding
st.markdown("""
    <style>
           .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 5rem;
                padding-right: 5rem;
            }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Clear Cypher Lab")
st.markdown("Welcome to the interactive cryptography and blockchain learning environment.")

# Creating the two main tabs
tab1, tab2 = st.tabs(["🌐 Clear ZKP", "⛓️ Blockchain"])

with tab1:
    st.header("Zero-Knowledge Proofs (ZKP)")
    st.info("Explore the world of privacy-preserving proofs.")
    
    zkp_module = st.radio("Select a Module:", ["Groth16", "ECC (Elliptic Curve Cryptography)"])
    
    if zkp_module == "Groth16":
        st.subheader("Groth16 Protocol")
        st.write("Groth16 is one of the most widely used zk-SNARK protocols.")
        
    elif zkp_module == "ECC (Elliptic Curve Cryptography)":
        st.subheader("Elliptic Curve Cryptography")
        st.write("ECC provides high security with smaller key sizes.")

with tab2:
    st.header("Blockchain Infrastructure")
    st.info("Foundational algorithms for distributed ledgers.")
    
    blc_module = st.radio("Select a Module:", ["RSA Encryption"])
    
    if blc_module == "RSA Encryption":
        st.subheader("RSA Algorithm")
        st.write("RSA is a fundamental public-key cryptosystem.")

st.divider()
st.caption("Clear Cypher Lab © 2026")
