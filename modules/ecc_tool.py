import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def run_ecc_visualizer():
    st.subheader("Elliptic Curve Visualizer")
    
    # Mathematical formula display
    st.latex(r"y^2 = x^3 + ax + b")
    
    # Layout: Left column for settings (Vertical), Right column for the plot
    # Ratio [1, 3] to keep the plot larger
    col_input, col_plot = st.columns([1, 3])
    
    with col_input:
        st.write("### Parameters")
        # Inputs are placed one after another to stay vertical
        a = st.number_input("a", value=-1.0, step=0.1, format="%.1f")
        b = st.number_input("b", value=1.0, step=0.1, format="%.1f")
        
        # Calculate Discriminant to check for singularity
        # Formula: Δ = 4a³ + 27b²
        discriminant = 4*(a**3) + 27*(b**2)
        
        if discriminant == 0:
            st.error("Δ=0: Singular Curve")
        else:
            st.info(f"Δ = {discriminant:.1f}")

    with col_plot:
        if discriminant != 0:
            # Generate meshgrid for the plot
            y, x = np.ogrid[-5:5:100j, -5:5:100j]
            
            # Figure size for a compact look
            fig, ax = plt.subplots(figsize=(5, 3))
            
            # Draw the elliptic curve contour
            ax.contour(x.ravel(), y.ravel(), y**2 - x**3 - a*x - b, [0], colors='royalblue')
            
            # Chart aesthetics (English comments)
            ax.set_title(f"Curve: a={a}, b={b}", fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.axhline(0, color='black', linewidth=0.8)
            ax.axvline(0, color='black', linewidth=0.8)
            ax.tick_params(labelsize=8)
            
            # Display the plot in the right column
            st.pyplot(fig)

    st.divider()
