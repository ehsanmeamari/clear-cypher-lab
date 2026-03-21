import streamlit as st

st.set_page_config(page_title="Clear Cypher Lab", page_icon="🛡️", layout="wide")

st.title("🛡️ Clear Cypher Lab")
st.markdown("Welcome to the interactive cryptography and blockchain learning environment.")

# Creating the two main tabs
tab1, tab2 = st.tabs(["🌐 Clear ZKP", "⛓️ Blockchain"])

with tab1:
    st.header("Zero-Knowledge Proofs (ZKP)")
    st.info("Explore the world of privacy-preserving proofs.")
    
    # Sub-sections for ZKP
    zkp_module = st.radio("Select a Module:", ["Groth16", "ECC (Elliptic Curve Cryptography)"])
    
    if zkp_module == "Groth16":
        st.subheader("Groth16 Protocol")
        st.write("Groth16 is one of the most widely used zk-SNARK protocols in blockchain projects like Zcash.")
        # You can add interactive logic for Groth16 here later
        
    elif zkp_module == "ECC (Elliptic Curve Cryptography)":
        st.subheader("Elliptic Curve Cryptography")
        st.write("ECC provides the same level of security as RSA but with much smaller key sizes.")

with tab2:
    st.header("Blockchain Infrastructure")
    st.info("Foundational algorithms for distributed ledgers.")
    
    # Sub-section for Blockchain
    blc_module = st.radio("Select a Module:", ["RSA Encryption"])
    
    if blc_module == "RSA Encryption":
        st.subheader("RSA Algorithm")
        st.write("RSA is a public-key cryptosystem that is widely used for secure data transmission.")
        # We can add an RSA generator here in the next step

st.divider()
st.caption("Clear Cypher Lab © 2026 - Educational Purpose")
