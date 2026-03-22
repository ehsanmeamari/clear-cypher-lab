import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# This line prevents Streamlit from showing a warning about global pyplot use
st.set_option('deprecation.showPyplotGlobalUse', False)

def run_ecc_visualizer():
    st.subheader("Elliptic Curve Visualizer")
    
    # Mathematical formula in standard LaTeX
    st.latex(r"y^2 = x^3 + ax + b")
    
    # Layout: Left for inputs, Right for the plot
    col_input, col_plot = st.columns([1, 2.5])
    
    with col_input:
        st.write("### Parameters")
        a = st.number_input("a", value=-1.0, step=0.1, format="%.1f")
        b = st.number_input("b", value=1.0, step=0.1, format="%.1f")
        
        # Discriminant check
        discriminant = 4*(a**3) + 27*(b**2)
        if discriminant == 0:
            st.error("Δ=0: Singular Curve")
        else:
            st.info(f"Δ = {discriminant:.1f}")

    with col_plot:
        if discriminant != 0:
            # 1. High-resolution rendering settings
            plt.rcParams['figure.dpi'] = 200
            plt.rcParams['mathtext.fontset'] = 'stix'
            plt.rcParams['font.family'] = 'STIXGeneral'
            
            # 2. Create figure with a clean look
            fig, ax = plt.subplots(figsize=(4, 3.5))
            
            # 3. Create a high-density meshgrid for smooth curves (500j)
            y, x = np.ogrid[-5:5:500j, -5:5:500j]
            
            # 4. Draw the curve with professional colors and thickness
            ax.contour(x.ravel(), y.ravel(), y**2 - x**3 - a*x - b, [0], 
                       colors='#3498db', linewidths=2)
            
            # 5. Smart Title Logic for LaTeX look
            a_sign = "-" if a < 0 else "+"
            b_sign = "-" if b < 0 else "+"
            title_text = fr"$y^2 = x^3 {a_sign} {abs(a)}x {b_sign} {abs(b)}$"
            ax.set_title(title_text, fontsize=11, pad=15)
            
            # 6. Aesthetic Grid and Axis (Minimalist style like Corbellini's)
            ax.grid(True, linestyle='-', alpha=0.15, color='#bdc3c7')
            ax.axhline(0, color='#7f8c8d', linewidth=0.8, alpha=0.4)
            ax.axvline(0, color='#7f8c8d', linewidth=0.8, alpha=0.4)
            
            # Remove the outer box (spines) for a modern feel
            for spine in ax.spines.values():
                spine.set_visible(False)
            
            ax.tick_params(axis='both', which='major', labelsize=8, colors='#95a5a6')
            
            # 7. Render with container width
            st.pyplot(fig, use_container_width=True)

    st.divider()
