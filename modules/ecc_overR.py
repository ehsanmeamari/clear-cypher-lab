import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def run_ecc_overR():
    st.subheader("Elliptic Curve Visualizer (Real Numbers)")
    
    # --- Layout: Two Main Columns ---
    col_left, col_right = st.columns([1.5, 2.5])
    
    with col_left:
        with st.expander("Curve Definition", expanded=True):
            # Input fields for parameters a and b
            a = st.number_input("Parameter (a)", value=-1.0, step=0.1, format="%.1f")
            b = st.number_input("Parameter (b)", value=1.0, step=0.1, format="%.1f")
            
            st.divider()
            
            # Discriminant Calculation and Error Handling
            discriminant = 4*(a**3) + 27*(b**2)
            
            if discriminant == 0:
                st.error("Singular Curve: Δ = 0. Please change parameters.")
            else:
                # Displaying the curve formula and Discriminant
                st.latex(f"E: y^2 = x^3 {'+' if a>=0 else ''} {a:.1f}x {'+' if b>=0 else ''} {b:.1f}")
                st.info(f"Discriminant (Δ) = {discriminant:.2f}")

    with col_right:
        # Only plot if the curve is non-singular
        if discriminant != 0:
            # High-quality rendering settings
            plt.rcParams['mathtext.fontset'] = 'stix'
            plt.rcParams['font.family'] = 'STIXGeneral'
            
            # Create figure and axis
            fig, ax = plt.subplots(figsize=(6, 5), dpi=150)
            
            # Create a meshgrid for plotting the implicit function
            y, x = np.ogrid[-5:5:500j, -5:5:500j]
            
            # Plot the elliptic curve: y^2 = x^3 + ax + b
            ax.contour(x.ravel(), y.ravel(), y**2 - x**3 - a*x - b, [0], 
                       colors='#3498db', linewidths=2.5)
            
            # Minimalist styling for the chart
            ax.grid(True, linestyle='--', alpha=0.3, color='#bdc3c7')
            ax.axhline(0, color='#7f8c8d', linewidth=1, alpha=0.5)
            ax.axvline(0, color='#7f8c8d', linewidth=1, alpha=0.5)
            
            # Hide the outer spines for a cleaner look
            for spine in ax.spines.values():
                spine.set_visible(False)
            
            ax.tick_params(axis='both', labelsize=9, colors='#95a5a6')
            
            # Render the plot in Streamlit
            st.pyplot(fig)
        else:
            st.warning("Increase/Decrease 'a' or 'b' to visualize the curve.")

    st.divider()
