import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def run_ecc_overR():
    st.subheader("Elliptic Curve Visualizer")
    
    # --- New Integrated Curve Definition Section ---
    with st.expander("Curve Definition", expanded=True):
        c1, c2, c3 = st.columns([1, 1, 2.5])            
        with c1: 
            a = st.number_input("Parameter (a)", value=-1.0, step=0.1, format="%.1f")
        with c2: 
            b = st.number_input("Parameter (b)", value=1.0, step=0.1, format="%.1f")

        with c3:
            discriminant = 4*(a**3) + 27*(b**2)
            if discriminant == 0:
                st.error("Singular Curve: Select another curve parameters")
            else:
                st.markdown("<div style='margin-top: 25px;'>", unsafe_allow_html=True)
                # Dynamic LaTeX formula for Real Numbers
                a_part = f"{a:+.1f}x" if a != 0 else ""
                b_part = f"{b:+.1f}" if b != 0 else ""
                st.latex(f"E: y^2 = x^3 {a_part} {b_part}")
                st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # --- Plotting Section ---
    # We use a single column or adjust layout as needed
    if discriminant != 0:
        # High-quality rendering settings
        plt.rcParams['mathtext.fontset'] = 'stix'
        plt.rcParams['font.family'] = 'STIXGeneral'
        
        # Create figure
        fig, ax = plt.subplots(figsize=(7, 4), dpi=150)
        
        # High-density meshgrid for smooth lines
        y, x = np.ogrid[-5:5:500j, -5:5:500j]
        
        # Plot curve
        ax.contour(x.ravel(), y.ravel(), y**2 - x**3 - a*x - b, [0], 
                   colors='#3498db', linewidths=2)
        
        # Dynamic Title
        a_sign = "-" if a < 0 else "+"
        b_sign = "-" if b < 0 else "+"
        title_text = fr"$y^2 = x^3 {a_sign} {abs(a):.1f}x {b_sign} {abs(b):.1f}$"
        ax.set_title(title_text, fontsize=10, pad=15)
        
        # Minimalist styling
        ax.grid(True, linestyle='-', alpha=0.1, color='#bdc3c7')
        ax.axhline(0, color='#7f8c8d', linewidth=0.8, alpha=0.3)
        ax.axvline(0, color='#7f8c8d', linewidth=0.8, alpha=0.3)
        
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        ax.tick_params(axis='both', labelsize=8, colors='#95a5a6')
        
        # Center the plot
        st.pyplot(fig)
        st.info(f"Discriminant (Δ) = {discriminant:.2f}")

    st.divider()
