import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def run_ecc_visualizer():
    st.subheader("Elliptic Curve Visualizer")
    st.latex(r"y^2 = x^3 + ax + b")
    
    # Create two narrow columns to put inputs side-by-side like your image
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Using a short label to keep it clean
        a = st.number_input("a", value=-1.0, step=0.1, format="%.1f")
        
    with col2:
        # Using a short label to keep it clean
        b = st.number_input("b", value=1.0, step=0.1, format="%.1f")

    # Math Logic: Discriminant check to avoid singular curves
    # Formula: Δ = 4a³ + 27b²
    discriminant = 4*(a**3) + 27*(b**2)
    
    if discriminant == 0:
        st.warning("⚠️ Singular curve (Δ=0). Please change a or b.")
    else:
        # Setup the mathematical grid for the plot
        y, x = np.ogrid[-5:5:100j, -5:5:100j]
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Draw the curve based on the equation: y² - x³ - ax - b = 0
        ax.contour(x.ravel(), y.ravel(), y**2 - x**3 - a*x - b, [0], colors='royalblue')
        
        # Grid and axis styling
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.axhline(0, color='black', linewidth=0.8)
        ax.axvline(0, color='black', linewidth=0.8)
        ax.set_title(f"Curve for a={a}, b={b}")
        
        # Display the finalized plot
        st.pyplot(fig)
        st.info(f"Discriminant (Δ): {discriminant:.2f}")
