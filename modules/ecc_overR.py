import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

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
            st.markdown("**Slope (s):** $s = (y_Q - y_P)/(x_Q - x_P)$ or $(3x_P^2 + a)/(2y_P)$")
            st.latex(r"x_R = s^2 - x_P - x_Q, \quad y_R = s(x_P - x_R) - y_P")

        # --- Section 3: Smart Calculator ---
        with st.expander("Point Addition Calculator", expanded=True):
            col_p, col_q = st.columns(2)
            
            # --- Point P Logic ---
            with col_p:
                st.markdown("<span style='color:red'>●</span> **Point P**", unsafe_allow_html=True)
                px = st.number_input("xP", value=1.0, step=0.1, key="px")
                y2_p = px**3 + a*px + b
                if y2_p >= 0:
                    py_val = math.sqrt(y2_p)
                    p_sign = st.radio("Sign of yP", ["+", "-"], key="p_sign", horizontal=True)
                    py = py_val if p_sign == "+" else -py_val
                    st.latex(f"y_P \approx {py:.3f}")
                else:
                    st.error("xP is out of curve domain")
                    py = None

            # --- Point Q Logic ---
            with col_q:
                st.markdown("<span style='color:orange'>●</span> **Point Q**", unsafe_allow_html=True)
                qx = st.number_input("xQ", value=0.0, step=0.1, key="qx")
                y2_q = qx**3 + a*qx + b
                if y2_q >= 0:
                    qy_val = math.sqrt(y2_q)
                    q_sign = st.radio("Sign of yQ", ["+", "-"], key="q_sign", horizontal=True)
                    qy = qy_val if q_sign == "+" else -qy_val
                    st.latex(f"y_Q \approx {qy:.3f}")
                else:
                    st.error("xQ is out of curve domain")
                    qy = None
            
            st.divider()
            res_xr, res_yr = None, None
            if py is not None and qy is not None:
                if st.button("Calculate R = P + Q", use_container_width=True):
                    try:
                        if px == qx and py == qy:
                            if py == 0: s = None
                            else: s = (3 * px**2 + a) / (2 * py)
                        elif px == qx: s = None
                        else: s = (qy - py) / (qx - px)
                        
                        if s is not None:
                            res_xr = s**2 - px - qx
                            res_yr = s * (px - res_xr) - py
                            st.success(f"Resulting Point R: $({res_xr:.3f}, {res_yr:.3f})$")
                    except ZeroDivisionError:
                        st.error("Point at infinity")

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
                
                y_m, x_m = np.ogrid[-plot_range:plot_range:500j, -plot_range:plot_range:500j]
                ax.contour(x_m.ravel(), y_m.ravel(), y_m**2 - x_m**3 - a*x_m - b, [0], colors='#3498db', linewidths=2.5)
                
                # Plot P and Q
                if py is not None:
                    ax.scatter(px, py, color='red', s=50, zorder=5, label='P')
                if qy is not None:
                    ax.scatter(qx, qy, color='orange', s=50, zorder=5, label='Q')
                
                # Plot R
                if res_xr is not None and abs(res_xr) < plot_range:
                    ax.scatter(res_xr, res_yr, color='green', s=70, marker='X', zorder=6, label='R')

                ax.set_xlim([-plot_range, plot_range]); ax.set_ylim([-plot_range, plot_range])
                ax.grid(True, linestyle='--', alpha=0.3); ax.axhline(0, color='grey', alpha=0.5); ax.axvline(0, color='grey', alpha=0.5)
                for spine in ax.spines.values(): spine.set_visible(False)
                st.pyplot(fig)

    st.divider()
