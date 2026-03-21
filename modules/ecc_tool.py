import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def run_ecc_visualizer():
    st.subheader("Elliptic Curve Visualizer")
    st.latex(r"y^2 = x^3 + ax + b")
    
    # Inputs in two columns
    col1, col2 = st.columns([1, 1])
    with col1:
        a = st.number_input("a", value=-1.0, step=0.1, format="%.1f")
    with col2:
        b = st.number_input("b", value=1.0, step=0.1, format="%.1f")

    # Math Logic: Discriminant check
    discriminant = 4*(a**3) + 27*(b**2)
    
    if discriminant == 0:
        st.warning("⚠️ Singular curve (Δ=0).")
    else:
        # Define grid for the plot
        y, x = np.ogrid[-5:5:100j, -5:5:100j]
        
        # KEY CHANGE: Reduced figsize to (4, 3) to make it half size
        fig, ax = plt.subplots(figsize=(4, 3))
        
        # Plotting logic
        ax.contour(x.ravel(), y.ravel(), y**2 - x**3 - a*x - b, [0], colors='royalblue')
        
        # Styling the plot
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.tick_params(axis='both', which='major', labelsize=8) # Smaller labels
        
        # Center the plot using Streamlit columns
        empty_col1, center_col, empty_col2 = st.columns([1, 2, 1])
        with center_col:
            st.pyplot(fig)
            
        st.info(f"Discriminant (Δ): {discriminant:.2f}")
