import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def run_ecc_visualizer():
    st.subheader("Elliptic Curve Visualizer")
    
    # Formula display
    st.latex(r"y^2 = x^3 + ax + b")
    
    # Column layout: Settings on the left, Plot on the right
    col_input, col_plot = st.columns([1, 2.5])
    
    with col_input:
        st.write("### Parameters")
        # Inputs stacked vertically
        a = st.number_input("a", value=-1.0, step=0.1, format="%.1f")
        b = st.number_input("b", value=1.0, step=0.1, format="%.1f")
        
        # Discriminant calculation
        discriminant = 4*(a**3) + 27*(b**2)
        
        if discriminant == 0:
            st.error("Δ=0: Singular Curve")
        else:
            st.info(f"Δ = {discriminant:.1f}")

    with col_plot:
        if discriminant != 0:
            y, x = np.ogrid[-5:5:100j, -5:5:100j]
            
            # SIZE: Changed to (1.0, 1.0) for a compact look
            fig, ax = plt.subplots(figsize=(1.0, 1.0))
            
            # Curve plotting
            ax.contour(x.ravel(), y.ravel(), y**2 - x**3 - a*x - b, [0], colors='royalblue')
            
            # Drawing the Curve
            # Force Matplotlib to use LaTeX-style font for all math text
            plt.rcParams['mathtext.fontset'] = 'stix'
            plt.rcParams['font.family'] = 'STIXGeneral'
    
            # Writting the formulla over the Curve
            a_sign = "-" if a < 0 else "+"
            b_sign = "-" if b < 0 else "+"            
            # We use abs(a) and abs(b) to avoid double signs like "+ -1.0"
            title_text = fr"$y^2 = x^3 {a_sign} {abs(a)}x {b_sign} {abs(b)}$"        
            ax.set_title(title_text, fontsize=6, pad=15)

            # Drawing the curve
            ax.grid(True, linestyle='--', alpha=0.4)
            ax.axhline(0, color='black', linewidth=0.6)
            ax.axvline(0, color='black', linewidth=0.6)
            
            # Shrink tick labels to fit the small frame
            ax.tick_params(labelsize=7)
            
            # Displaying the plot
            st.pyplot(fig)

    st.divider()
