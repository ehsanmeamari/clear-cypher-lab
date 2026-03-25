import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

def run_ecc_overR():
    st.subheader("Elliptic Curve Visualizer (Real Numbers)")
    
    # --- Layout: Two Main Columns ---
    col_left, col_right = st.columns([2, 2.5])
    
    with col_left:
        # --- Section 1: Curve Definition ---
        with st.expander("Curve Definition", expanded=True):
            input_row = st.columns([1, 1, 2])
            with input_row[0]:
                a = st.number_input("a", value=-1.0, step=0.1, format="%.1f", key="ecc_r_a")
            with input_row[1]:
                b = st.number_input("b", value=1.0, step=0.1, format="%.1f", key="ecc_r_b")
            
            discriminant = 4*(a**3) + 27*(b**2)
            if discriminant != 0:
                with input_row[2]:
                    st.markdown("<div style='padding-top: 25px;'>", unsafe_allow_html=True)
                    a_part = f"{a:+.1f}x" if a != 0 else ""
                    b_part = f"{b:+.1f}" if b != 0 else ""
                    st.latex(f"y^2 = x^3 {a_part} {b_part}")
                    st.markdown("</div>", unsafe_allow_html=True)
            
            st.divider()
            if discriminant == 0: st.error("Singular Curve: Δ = 0")
            else: st.info(f"Discriminant (Δ) = {discriminant:.2f}")

        # --- Section 3: Smart Bi-directional Calculator ---
        with st.expander("Point Addition Calculator", expanded=True):
            
            def get_point_coords(label, key_suffix, color):
                st.markdown(f"<span style='color:{color}'>●</span> **Point {label}**", unsafe_allow_html=True)
                mode = st.radio(f"Input mode for {label}", ["Input X", "Input Y"], key=f"mode_{key_suffix}", horizontal=True)
                
                final_x, final_y = None, None
                
                if mode == "Input X":
                    xin = st.number_input(f"x{label}", value=1.0 if label=="P" else 0.0, step=0.1, key=f"x{key_suffix}")
                    rhs = xin**3 + a*xin + b
                    if rhs >= 0:
                        y_val = math.sqrt(rhs)
                        sign = st.radio(f"Sign of y{label}", ["+", "-"], key=f"s{key_suffix}", horizontal=True)
                        final_x, final_y = xin, (y_val if sign == "+" else -y_val)
                        st.caption(f"Calculated: y ≈ {final_y:.3f}")
                    else:
                        st.error(f"x{label} is out of domain")
                else:
                    yin = st.number_input(f"y{label}", value=1.0 if label=="P" else 0.5, step=0.1, key=f"y{key_suffix}")
                    # Solve x^3 + ax + (b - y^2) = 0
                    coeffs = [1, 0, a, (b - yin**2)]
                    roots = np.roots(coeffs)
                    real_roots = [r.real for r in roots if np.isreal(r)]
                    
                    if real_roots:
                        selected_x = st.selectbox(f"Select possible x{label}", sorted(real_roots), format_func=lambda x: f"{x:.3f}", key=f"sel{key_suffix}")
                        final_x, final_y = selected_x, yin
                    else:
                        st.error(f"No real X found for y={yin}")
                
                return final_x, final_y

            col_p, col_q = st.columns(2)
            with col_p: px, py = get_point_coords("P", "p", "red")
            with col_q: qx, qy = get_point_coords("Q", "q", "orange")
            
            st.divider()
            res_xr, res_yr = None, None
            if px is not None and py is not None and qx is not None and qy is not None:
                if st.button("Calculate R = P + Q", use_container_width=True):
                    try:
                        if abs(px - qx) < 1e-9 and abs(py - qy) < 1e-9:
                            if abs(py) < 1e-9: s = None
                            else: s = (3 * px**2 + a) / (2 * py)
                        elif abs(px - qx) < 1e-9: s = None
                        else: s = (qy - py) / (qx - px)
                        
                        if s is not None:
                            res_xr = s**2 - px - qx
                            res_yr = s * (px - res_xr) - py
                            st.success(f"Result R: $({res_xr:.3f}, {res_yr:.3f})$")
                        else: st.error("Result is Point at Infinity")
                    except ZeroDivisionError: st.error("Error in calculation")

    with col_right:
        with st.expander("Visualizer", expanded=True):
            r_col1, r_col2 = st.columns([1, 1])
            with r_col1: st.markdown("<p style='padding-top: 5px; font-weight: bold;'>🔍 Plot Range (±)</p>", unsafe_allow_html=True)
            with r_col2: plot_range = st.number_input("", value=5, min_value=1, step=1, key="combined_range", label_visibility="collapsed")
            
            st.divider()
            if discriminant != 0:
                plt.rcParams['mathtext.fontset'] = 'stix'
                fig, ax = plt.subplots(figsize=(6, 5), dpi=150)
                y_m, x_m = np.ogrid[-plot_range:plot_range:500j, -plot_range:plot_range:500j]
                ax.contour(x_m.ravel(), y_m.ravel(), y_m**2 - x_m**3 - a*x_m - b, [0], colors='#3498db', linewidths=2.5)
                
                if py is not None: ax.scatter(px, py, color='red', s=50, zorder=5)
                if qy is not None: ax.scatter(qx, qy, color='orange', s=50, zorder=5)
                if res_xr is not None and abs(res_xr) < plot_range and abs(res_yr) < plot_range:
                    ax.scatter(res_xr, res_yr, color='green', s=80, marker='X', zorder=6)
                
                ax.set_xlim([-plot_range, plot_range]); ax.set_ylim([-plot_range, plot_range])
                ax.grid(True, linestyle='--', alpha=0.3)
                ax.axhline(0, color='grey', alpha=0.3); ax.axvline(0, color='grey', alpha=0.3)
                for spine in ax.spines.values(): spine.set_visible(False)
                st.pyplot(fig)

    st.divider()
