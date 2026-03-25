import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def run_ecc_overR():
    st.subheader("Elliptic Curve Visualizer (Real Numbers)")
    
    # --- Layout: Two Main Columns ---
    col_left, col_right = st.columns([1.8, 2.5])
    
    with col_left:
        with st.expander("Curve Definition", expanded=True):
            # Row 1: Parameters and Equation
            input_row = st.columns([1, 1, 2])
            with input_row[0]:
                a = st.number_input("a", value=-1.0, step=0.1, format="%.1f", key="ecc_r_a")
            with input_row[1]:
                b = st.number_input("b", value=1.0, step=0.1, format="%.1f", key="ecc_r_b")
            
            discriminant = 4*(a**3) + 27*(b**2)
            
            with input_row[2]:
                if discriminant != 0:
                    st.markdown("<div style='padding-top: 25px;'>", unsafe_allow_html=True)
                    a_part = f"{a:+.1f}x" if a != 0 else ""
                    b_part = f"{b:+.1f}" if b != 0 else ""
                    st.latex(f"y^2 = x^3 {a_part} {b_part}")
                    st.markdown("</div>", unsafe_allow_html=True)

            st.divider()
            
            if discriminant == 0:
                st.error("Singular Curve: Δ = 0")
            else:
                st.info(f"Discriminant (Δ) = {discriminant:.2f}")

    with col_right:
        # Putting everything inside the Visualizer expander
        with st.expander("Visualizer", expanded=True):
            # Plot Range Settings placed ABOVE the chart
            st.write("🔍 **Plot Range Settings**")
            range_col1, range_col2 = st.columns(2)
            with range_col1:
                x_range = st.number_input("x-axis range (±)", value=5, min_value=1, step=1, key="xr")
            with range_col2:
                y_range = st.number_input("y-axis range (±)", value=5, min_value=1, step=1, key="yr")
            
            st.divider()

            if discriminant != 0:
                plt.rcParams['mathtext.fontset'] = 'stix'
                plt.rcParams['font.family'] = 'STIXGeneral'
                
                fig, ax = plt.subplots(figsize=(6, 4.5), dpi=150)
                
                # Dynamic meshgrid based on user input
                y, x = np.ogrid[-y_range:y_range:500j, -x_range:x_range:500j]
                
                # Plot the curve: y^2 - x^3 - ax - b = 0
                ax.contour(x.ravel(), y.ravel(), y**2 - x**3 - a*x - b, [0], 
                           colors='#3498db', linewidths=2.5)
                
                # Set axis limits precisely
                ax.set_xlim([-x_range, x_range])
                ax.set_ylim([-y_range, y_range])
                
                # Minimalist styling
                ax.grid(True, linestyle='--', alpha=0.3, color='#bdc3c7')
                ax.axhline(0, color='#7f8c8d', linewidth=1, alpha=0.5)
                ax.axvline(0, color='#7f8c8d', linewidth=1, alpha=0.5)
                
                for spine in ax.spines.values():
                    spine.set_visible(False)
                
                ax.tick_params(axis='both', labelsize=9, colors='#95a5a6')
                
                st.pyplot(fig)
            else:
                st.warning("Please adjust parameters in 'Curve Definition' to see the plot.")

    st.divider()
