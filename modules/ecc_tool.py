import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def run_ecc_visualizer():
    st.subheader("Elliptic Curve Visualizer")
    st.latex(r"y^2 = x^3 + ax + b")
    
    # Input layout for curve parameters
    col1, col2 = st.columns(2)
    with col1:
        # User can type the value for 'a'
        a = st.number_input("Enter parameter a:", value=-1.0, step=0.1)
    with col2:
        # User can type the value for 'b'
        b = st.number_input("Enter parameter b:", value=1.0, step=0.1)

    # Check for singular curve condition: 4a^3 + 27b^2 must not be 0
    discriminant = 4*(a**3) + 27*(b**2)
    
    if discriminant == 0:
        st.warning("⚠️ Singular curve detected (4a³ + 27b² = 0). Please adjust a or b.")
    else:
        # Create a grid for plotting
        y, x = np.ogrid[-5:5:100j, -5:5:100j]
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Plot the contour where the elliptic curve equation holds true
        ax.contour(x.ravel(), y.ravel(), y**2 - x**3 - a*x - b, [0], colors='royalblue')
        
        # Aesthetic plot settings
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.set_title(f"Elliptic Curve: $y^2 = x^3 + ({a})x + ({b})$")
        
        # Render plot in Streamlit
        st.pyplot(fig)
        st.info(f"The Discriminant is: {discriminant:.2f}")
