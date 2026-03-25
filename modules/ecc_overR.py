import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def run_ecc_overR():
    st.subheader("Elliptic Curve Visualizer (Real Numbers)")
    
    # --- Layout: Two Main Columns ---
    col_left, col_right = st.columns([2, 2])
    
    with col_left:
        # --- Section 1: Curve Definition ---
        with st.expander("Curve Definition", expanded=True):
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

        # --- Section 2: Point Addition Formulas ---
        with st.expander("Point Addition Formulas", expanded=False):
            st.markdown("**Case 1: $P \\neq Q$ (Addition)**")
            st.latex(r"s = \frac{y_Q - y_P}{x_Q - x_P}")
            st.markdown("**Case 2: $P = Q$ (Doubling)**")
            st.latex(r"s = \frac{3x_P^2 + a}{2y_P}")
            st.markdown("**Resulting Point R:**")
            st.latex(r"x_R = s^2 - x_P - x_Q")
            st.latex(r"y_R = s(x_P - x_R) - y_P")

        # --- Section 3: Calculator (Point Addition) ---
        with st.expander("Point Addition Calculator", expanded=True):
            col_p, col_q = st.columns(2)
            with col_p:
                st.markdown("**Point P**")
                px = st.number_input("xP", value=0.0, step=0.1, key="px")
                py = st.number_input("yP", value=0.0, step=0.1, key="py")
            with col_q:
                st.markdown("**Point Q**")
                qx = st.number_input("xQ", value=0.0, step=0.1, key="qx")
                qy = st.number_input("yQ", value=0.0, step=0.1, key="qy")
            
            if st.button("Calculate R = P + Q", use_container_width=True):
                try:
                    # Check if points are on the curve (Optional but recommended)
                    # Check P: y^2 = x^3 + ax + b
                    if abs(py**2 - (px**3 + a*px + b)) > 0.1:
                        st.warning("Note: Point P is not exactly on the curve.")
                    
                    if px == qx and py == qy:
                        # Case P = Q (Doubling)
                        if py == 0:
                            st.error("Point at Infinity: Vertical tangent at y=0")
                            s = None
                        else:
                            s = (3 * px**2 + a) / (2 * py)
                    elif px == qx:
                        # Vertical line
                        st.error("Result is Point at Infinity (Vertical Line)")
                        s = None
                    else:
                        # Case P != Q (Addition)
                        s = (qy - py) / (qx - px)
                    
                    if s is not None:
                        xr = s**2 - px - qx
                        yr = s * (px - xr) - py
                        st.success(f"Resulting Point R: $({xr:.3f}, {yr:.3f})$")
                except ZeroDivisionError:
                    st.error("Error: Division by zero (Point at infinity)")

    with col_right:
        # --- Section 4: Visualizer ---
        with st.expander("Visualizer", expanded=True):
            r_col1, r_col2 = st.columns([1, 1])
            with r_col1:
                st.markdown("<p style='padding-top: 5px; font-weight: bold;'>🔍 Plot Range (±)</p>", unsafe_allow_html=True)
            with r_col2:
                plot_range = st.number_input("", value=5, min_value=1, step=1, key="combined_range", label_visibility="collapsed")
            
            st.divider()

            if discriminant != 0:
                plt.rcParams['mathtext.fontset'] = 'stix'
                plt.rcParams['font.family'] = 'STIXGeneral'
                fig, ax = plt.subplots(figsize=(6, 4.5), dpi=150)
                y_mesh, x_mesh = np.ogrid[-plot_range:plot_range:500j, -plot_range:plot_range:500j]
                ax.contour(x_mesh.ravel(), y_mesh.ravel(), y_mesh**2 - x_mesh**3 - a*x_mesh - b, [0], 
                           colors='#3498db', linewidths=2.5)
                
                # Optional: Plot the points P and Q on the graph
                # ax.scatter([px, qx], [py, qy], color='red', zorder=5)
                
                ax.set_xlim([-plot_range, plot_range])
                ax.set_ylim([-plot_range, plot_range])
                ax.grid(True, linestyle='--', alpha=0.3, color='#bdc3c7')
                ax.axhline(0, color='#7f8c8d', linewidth=1, alpha=0.5)
                ax.axvline(0, color='#7f8c8d', linewidth=1, alpha=0.5)
                for spine in ax.spines.values(): spine.set_visible(False)
                ax.tick_params(axis='both', labelsize=9, colors='#95a5a6')
                st.pyplot(fig)

    st.divider()
