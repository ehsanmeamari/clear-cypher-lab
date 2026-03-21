import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Clear Cypher Lab", page_icon="🛡️", layout="wide")

# CSS for a clean look and top padding
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
    st.header("Groth16 & ECC")
    zkp_module = st.radio("Select a Module:", ["Extension Field", "ECC Visualizer"])
    
    if zkp_module == "Extension Field":
        st.subheader("Extension Field")
        st.write("Extension Fields are fundamental in pairing-based cryptography used in ZKPs.")
        st.info("Coming Soon: Interactive Field Operations.")
        
    elif zkp_module == "ECC Visualizer":
        st.subheader("Elliptic Curve Visualizer")
        st.latex(r"y^2 = x^3 + ax + b")
        
        # User inputs for a and b
        col1, col2 = st.columns(2)
        with col1:
            a = st.slider("Parameter a:", -5, 5, -1)
        with col2:
            b = st.slider("Parameter b:", -5, 5, 1)

        # Plotting the curve
        y, x = np.ogrid[-5:5:100j, -5:5:100j]
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.contour(x.ravel(), y.ravel(), y**2 - x**3 - a*x - b, [0], colors='royalblue')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.set_title(f"Curve: $y^2 = x^3 + ({a})x + ({b})$")
        
        st.pyplot(fig)

with tab2:
    st.header("Blockchain Infrastructure")
    blc_module = st.radio("Select a Module:", ["RSA Practical"])
    
    if blc_module == "RSA Practical":
        st.subheader("RSA Encryption Demo")
        message = st.text_input("Enter message to encrypt:", "Hello")
        if message:
            encrypted = '-'.join([hex(ord(c)) for c in message])
            st.success(f"Encrypted (Hex): {encrypted}")

st.divider()
st.caption("Clear Cypher Lab © 2026")
