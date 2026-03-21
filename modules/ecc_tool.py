import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def run_ecc_visualizer():
    st.subheader("Elliptic Curve Visualizer")
    st.latex(r"y^2 = x^3 + ax + b")
    
    col1, col2 = st.columns(2)
    with col1:
        # تغییر از slider به number_input
        a = st.number_input("Enter parameter a:", value=-1.0, step=0.1)
    with col2:
        b = st.number_input("Enter parameter b:", value=1.0, step=0.1)

    # بررسی شرط نان-سینگولار بودن (منحنی نباید گره یا لبه تیز داشته باشد)
    discriminant = 4*(a**3) + 27*(b**2)
    
    if discriminant == 0:
        st.warning("⚠️ This combination (4a³ + 27b² = 0) results in a singular curve. Please change a or b.")
    else:
        y, x = np.ogrid[-5:5:100j, -5:5:100j]
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # رسم منحنی
        ax.contour(x.ravel(), y.ravel(), y**2 - x**3 - a*x - b, [0], colors='royalblue')
        
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.set_title(f"Curve: $y^2 = x^3 + ({a})x + ({b})$")
        
        st.pyplot(fig)
        st.info(f"Discriminant: {discriminant:.2f}")
