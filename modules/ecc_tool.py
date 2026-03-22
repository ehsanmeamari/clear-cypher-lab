import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def run_ecc_visualizer():
    st.subheader("Elliptic Curve Visualizer")
    st.latex(r"y^2 = x^3 + ax + b")
    
    col_input, col_plot = st.columns([1, 2.5])
    
    with col_input:
        st.write("### Parameters")
        a = st.number_input("a", value=-1.0, step=0.1, format="%.1f")
        b = st.number_input("b", value=1.0, step=0.1, format="%.1f")
        
        discriminant = 4*(a**3) + 27*(b**2)
        if discriminant == 0:
            st.error("Δ=0: Singular Curve")
        else:
            st.info(f"Δ = {discriminant:.1f}")

    with col_plot:
        if discriminant != 0:
            # High-quality rendering settings
            plt.rcParams['mathtext.fontset'] = 'stix'
            plt.rcParams['font.family'] = 'STIXGeneral'
            
            # Create figure
            fig, ax = plt.subplots(figsize=(5, 4), dpi=150) # dpi=150 helps with clarity
            
            # High-density meshgrid for smooth lines
            y, x = np.ogrid[-5:5:500j, -5:5:500j]
            
            # Plot curve
            ax.contour(x.ravel(), y.ravel(), y**2 - x**3 - a*x - b, [0], 
                       colors='#3498db', linewidths=2)
            
            # Professional LaTeX Title
            a_sign = "-" if a < 0 else "+"
            b_sign = "-" if b < 0 else "+"
            title_text = fr"$y^2 = x^3 {a_sign} {abs(a)}x {b_sign} {abs(b)}$"
            ax.set_title(title_text, fontsize=12, pad=15)
            
            # Minimalist styling (like the reference site)
            ax.grid(True, linestyle='-', alpha=0.1, color='#bdc3c7')
            ax.axhline(0, color='#7f8c8d', linewidth=0.8, alpha=0.3)
            ax.axvline(0, color='#7f8c8d', linewidth=0.8, alpha=0.3)
            
            for spine in ax.spines.values():
                spine.set_visible(False)
            
            ax.tick_params(axis='both', labelsize=8, colors='#95a5a6')
            
            # Crucial: pass the 'fig' object directly to avoid the warning/error
            st.pyplot(fig) 

    st.divider()
