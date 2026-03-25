import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

def run_ecc_overR():
    st.subheader("Elliptic Curve Visualizer (Real Numbers)")
    
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

        # --- Section 2: Smart Calculator ---
        with st.expander("Point Addition Calculator", expanded=True):
            def get_point_coords(label, key_suffix, color):
                st.markdown(f"<span style='color:{color}'>●</span> **Point {label}**", unsafe_allow_html=True)
                mode = st.radio(f"Input mode {label}", ["X", "Y"], key=f"mode_{key_suffix}", horizontal=True)
                fx, fy = None, None
                if mode == "X":
                    xin = st.number_input(f"x{label}", value=1.0 if label=="P" else 0.0, step=0.1, key=f"x{key_suffix}")
                    rhs = xin**3 + a*xin + b
                    if rhs >= 0:
                        y_val = math.sqrt(rhs)
                        sign = st.radio(f"Sign y{label}", ["+", "-"], key=f"s{key_suffix}", horizontal=True)
                        fx, fy = xin, (y_val if sign == "+" else -y_val)
                    else: st.error(f"x{label} out of domain")
                else:
                    yin = st.number_input(f"y{label}", value=1.0 if label=="P" else 0.5, step=0.1, key=f"y{key_suffix}")
                    roots = np.roots([1, 0, a, (b - yin**2)])
                    real_roots = [r.real for r in roots if np.isreal(r)]
                    if real_roots:
                        fx = st.selectbox(f"Select x{label}", sorted(real_roots), format_func=lambda x: f"{x:.3f}", key=f"sel{key_suffix}")
                        fy = yin
                return fx, fy

            col_p, col_q = st.columns(2)
            with col_p: px, py = get_point_coords("P", "p", "red")
            with col_q: qx, qy = get_point_coords("Q", "q", "orange")
            
            st.divider()
            res_xr, res_yr, s_val = None, None, None
            if px is not None and py is not None and qx is not None and qy is not None:
                if st.button("Calculate R = P + Q", use_container_width=True):
                    try:
                        if abs(px - qx) < 1e-9 and abs(py - qy) < 1e-9:
                            if abs(py) < 1e-9: s_val = None
                            else: s_val = (3 * px**2 + a) / (2 * py)
                        elif abs(px - qx) < 1e-9: s_val = None
                        else: s_val = (qy - py) / (qx - px)
                        
                        if s_val is not None:
                            res_xr = s_val**2 - px - qx
                            res_yr = s_val * (px - res_xr) - py
                            st.success(f"Result R: $({res_xr:.3f}, {res_yr:.3f})$")
                        else: st.error("Result is Point at Infinity")
                    except ZeroDivisionError: st.error("Calculation Error")

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
                
                # --- Drawing the Line through P and Q ---
                if s_val is not None:
                    # Line equation: y - py = s(x - px) => y = s*x - s*px + py
                    x_vals = np.array([-plot_range, plot_range])
                    y_vals = s_val * (x_vals - px) + py
                    ax.plot(x_vals, y_vals, color='#9b59b6', linestyle='--', linewidth=1, alpha=0.7, label='Secant/Tangent Line')
                    
                    # Optional: Plot the intersection point before reflection (Point -R)
                    ax.scatter(res_xr, -res_yr, facecolors='none', edgecolors='grey', s=50, zorder=4)

                # Plot P, Q, and R
                if py is not None: ax.scatter(px, py, color='red', s=60, zorder=5, label='P')
                if qy is not None: ax.scatter(qx, qy, color='orange', s=60, zorder=5, label='Q')
                if res_xr is not None and abs(res_xr) < plot_range and abs(res_yr) < plot_range:
                    ax.scatter(res_xr, res_yr, color='#2ecc71', s=100, marker='X', zorder=6, label='R = P+Q')
                    # Draw vertical line for reflection
                    ax.plot([res_xr, res_xr], [-res_yr, res_yr], color='grey', linestyle=':', linewidth=1, alpha=0.5)

                ax.set_xlim([-plot_range, plot_range]); ax.set_ylim([-plot_range, plot_range])
                ax.grid(True, linestyle='--', alpha=0.3)
                ax.axhline(0, color='grey', alpha=0.3); ax.axvline(0, color='grey', alpha=0.3)
                for spine in ax.spines.values(): spine.set_visible(False)
                st.pyplot(fig)
            else: st.warning("Adjust parameters to see the plot.")

    st.divider()
