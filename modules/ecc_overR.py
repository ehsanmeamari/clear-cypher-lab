import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

def run_ecc_overR():
    col_left, col_right = st.columns([2, 2])
    
    # --- Helper function for Point Addition ---
    def add_points(x1, y1, x2, y2, a):
        if x1 is None: return x2, y2
        if x2 is None: return x1, y1
        try:
            if abs(x1 - x2) < 1e-9 and abs(y1 - y2) < 1e-9:
                if abs(y1) < 1e-9: return None, None
                s = (3 * x1**2 + a) / (2 * y1)
            elif abs(x1 - x2) < 1e-9:
                return None, None
            else:
                s = (y2 - y1) / (x2 - x1)
            
            xr = s**2 - x1 - x2
            yr = s * (x1 - xr) - y1
            return xr, yr, s # Return slope for drawing line
        except ZeroDivisionError:
            return None, None, None

    # --- Scalar Multiplication (Double-and-Add) ---
    def scalar_mult(n, px, py, a):
        qx, qy = px, py
        rx, ry = None, None
        n = int(n)
        while n > 0:
            if n % 2 == 1:
                res = add_points(rx, ry, qx, qy, a)
                rx, ry = res[0], res[1]
            res_double = add_points(qx, qy, qx, qy, a)
            qx, qy = res_double[0], res_double[1]
            n //= 2
        return rx, ry

    with col_left:
        # --- Section 1: Curve Definition ---
        with st.expander("Curve Definition", expanded=True):
            input_row = st.columns([1, 1, 2])
            with input_row[0]: a = st.number_input("a", value=-1.0, step=0.1, format="%.1f", key="ecc_r_a")
            with input_row[1]: b = st.number_input("b", value=1.0, step=0.1, format="%.1f", key="ecc_r_b")
            
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

        # --- Reusable Input Logic ---
        def get_point_input(label, suffix, color, default_x=1.0):
            st.markdown(f"<span style='color:{color}'>●</span> **Point {label}**", unsafe_allow_html=True)
            mode = st.radio(f"Input mode {label}", ["X", "Y"], key=f"m_{suffix}", horizontal=True)
            fx, fy = None, None
            if mode == "X":
                xin = st.number_input(f"x{label}", value=default_x, step=0.1, key=f"x_{suffix}")
                rhs = xin**3 + a*xin + b
                if rhs >= 0:
                    y_val = math.sqrt(rhs)
                    sign = st.radio(f"Sign y{label}", ["+", "-"], key=f"s_{suffix}", horizontal=True)
                    fx, fy = xin, (y_val if sign == "+" else -y_val)
                    st.caption(f"Calculated y: {fy:.3f}")
                else: st.error(f"x{label} out of domain")
            else:
                yin = st.number_input(f"y{label}", value=1.0, step=0.1, key=f"y_{suffix}")
                roots = np.roots([1, 0, a, (b - yin**2)])
                real_roots = [r.real for r in roots if np.isreal(r)]
                if real_roots:
                    fx = st.selectbox(f"Select x{label}", sorted(real_roots), format_func=lambda x: f"{x:.3f}", key=f"sel_{suffix}")
                    fy = yin
            return fx, fy

        # --- Section 2: Point Addition Calculator ---
        with st.expander("Point Addition Calculator", expanded=False):
            col_p, col_q = st.columns(2)
            with col_p: px_add, py_add = get_point_input("P", "add_p", "red", default_x=1.0)
            with col_q: qx_add, qy_add = get_point_input("Q", "add_q", "orange", default_x=0.0)
            
            res_add_x, res_add_y, add_slope = None, None, None
            if st.button("Calculate P + Q", use_container_width=True):
                if px_add is not None and qx_add is not None:
                    res_add_x, res_add_y, add_slope = add_points(px_add, py_add, qx_add, qy_add, a)
                    if res_add_x is not None:
                        st.success(f"P + Q = ({res_add_x:.3f}, {res_add_y:.3f})")
                    else: st.error("Result is Point at Infinity")

        # --- Section 3: Scalar Multiplication Calculator ---
        with st.expander("Scalar Multiplication", expanded=True):
            px_s, py_s = get_point_input("P", "scaler", "blue", default_x=1.0)
            n_val = st.number_input("Multiplier (n)", min_value=1, value=2, step=1)
            
            res_nx, res_ny = None, None
            if st.button(f"Calculate {n_val}P", use_container_width=True):
                if px_s is not None:
                    res_nx, res_ny = scalar_mult(n_val, px_s, py_s, a)
                    if res_nx is not None:
                        st.success(f"{n_val}P = ({res_nx:.3f}, {res_ny:.3f})")

    with col_right:
        with st.expander("Visualizer", expanded=True):
            plot_range = st.number_input("🔍 Plot Range (±)", value=5, min_value=1, step=1, key="combined_range")
            st.divider()
            if discriminant != 0:
                plt.rcParams['mathtext.fontset'] = 'stix'
                fig, ax = plt.subplots(figsize=(6, 5), dpi=150)
                y_m, x_m = np.ogrid[-plot_range:plot_range:500j, -plot_range:plot_range:500j]
                ax.contour(x_m.ravel(), y_m.ravel(), y_m**2 - x_m**3 - a*x_m - b, [0], colors='#3498db', linewidths=2.5)
                
                # --- Drawing Addition Line & Vertical Reflection ---
                if add_slope is not None:
                    x_line = np.array([-plot_range, plot_range])
                    y_line = add_slope * (x_line - px_add) + py_add
                    ax.plot(x_line, y_line, color='#9b59b6', linestyle='--', linewidth=1, alpha=0.6)
                    # Vertical line from -R to R
                    ax.plot([res_add_x, res_add_x], [-res_add_y, res_add_y], color='grey', linestyle=':', alpha=0.5)
                    # Point -R (intersection before reflection)
                    ax.scatter(res_add_x, -res_add_y, facecolors='none', edgecolors='grey', s=40, zorder=4)

                # Plot Addition Points
                if py_add is not None:
                    ax.scatter(px_add, py_add, color='red', s=50, zorder=5, label='P')
                    ax.scatter(qx_add, qy_add, color='orange', s=50, zorder=5, label='Q')
                if res_add_x is not None:
                    ax.scatter(res_add_x, res_add_y, color='green', s=90, marker='X', zorder=6, label='P+Q')

                # Plot Multiplication Points
                if py_s is not None:
                    ax.scatter(px_s, py_s, color='blue', s=50, zorder=5, label='P(Mult)')
                if res_nx is not None:
                    ax.scatter(res_nx, res_ny, color='purple', s=90, marker='D', zorder=6, label=f'{n_val}P')

                ax.set_xlim([-plot_range, plot_range]); ax.set_ylim([-plot_range, plot_range])
                ax.grid(True, linestyle='--', alpha=0.3); ax.axhline(0, color='grey', alpha=0.2); ax.axvline(0, color='grey', alpha=0.2)
                for spine in ax.spines.values(): spine.set_visible(False)
                st.pyplot(fig)

    st.divider()
