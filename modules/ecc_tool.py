import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def run_ecc_visualizer():
    st.subheader("Elliptic Curve Visualizer")
    st.latex(r"y^2 = x^3 + ax + b")
    
    col1, col2 = st.columns(2)
    with col1:
        a = st.slider("Parameter a:", -5, 5, -1)
    with col2:
        b = st.slider("Parameter b:", -5, 5, 1)

    y, x = np.ogrid[-5:5:100j, -5:5:100j]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.contour(x.ravel(), y.ravel(), y**2 - x**3 - a*x - b, [0], colors='royalblue')
    ax.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)
