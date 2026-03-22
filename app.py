# Main Content
st.title("🛡️ Clear Cypher Lab")
st.markdown("Welcome to the interactive cryptography learning environment.")

# Corrected Tabs definition
tab1, tab2, tab3 = st.tabs(["🌐 Cryptography", "⛓️ Blockchain", "🔐 ZKP"])

with tab1:
    st.header("Cryptography")
    st.info("🚀 Advanced cryptography modules are under development.")
    st.write("""
    Upcoming tools:
    * RSA Key Generation & Encryption
    * Signature Schemes (ECDSA, Ed25519)
    """)

with tab2:
    st.header("Blockchain Infrastructure")
    st.info("🚀 Blockchain simulation tools coming soon.")
    st.write("""
    Planned features:
    * Merkle Tree Visualizer
    * Block Header Hashing (SHA-256)
    """)

with tab3:
    st.header("Zero-Knowledge Proofs (ZKP)")
    
    zkp_module = st.radio(
        "Select a Module:", 
        ["Modular Arithmetic", "Extension Field", "ECC", "Weil Pairing", "Lagrange Interpolation"], 
        key="zkp_main",
        horizontal=True # این گزینه باعث می‌شود منو افقی و زیباتر شود
    )
    
    st.divider()

    if zkp_module == "Modular Arithmetic":
        st.subheader("Modular Arithmetic")
        st.info("Visualizing Modulo operations and Finite Fields - Coming soon.")     

    elif zkp_module == "Extension Field":
        st.subheader("Extension Field")
        st.write("Extension Fields are fundamental in ZKP pairing-based cryptography.")       
        
    elif zkp_module == "ECC":
        ecc_sub_module = st.selectbox(
            "ECC Operations:", 
            ["Visualizer", "Point Addition", "Scalar Multiplication"]
        )
        if ecc_sub_module == "Visualizer":
            run_ecc_visualizer()
        else:
            st.info(f"{ecc_sub_module} module is under development.")

    elif zkp_module == "Weil Pairing":
        st.subheader("Weil Pairing")
        st.write("Weil Pairing coming soon.")

    elif zkp_module == "Lagrange Interpolation":
        st.subheader("Lagrange Interpolation")
        st.write("Lagrange Interpolation coming soon.") 

st.divider()
