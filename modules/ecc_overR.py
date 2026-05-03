import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

def run_ecc_overR():    
    # --- Custom CSS for Cream Styling ---
    st.markdown("""
        <style>
        /* Styling the header of expanders to be cream-colored */
        div[data-testid="stExpander"] details summary {
            background-color: #FDF5E6; /* OldLace color */
            border-radius: 5px;
            padding: 10px;
        }
        /* Optional: Border styling for the expander container */
        div[data-testid="stExpander"] {
            border: 1px solid #e6e6e6;
            border-radius: 5px;
            background-color: transparent;
        }
        </style>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 2.5])
    
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
            return xr, yr, s 
        except ZeroDivisionError:
            return None, None, None

    # --- Scalar Multiplication ---
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
        with st.expander("Curve Definition", expanded=False):
            input_row = st.columns([1, 1, 2])
            with input_row[0]: a = st.number_input("a", value=-1.0, step=0.1, key="ecc_r_a")
            with input_row[1]: b = st.number_input("b", value=1.0, step=0.1, key="ecc_r_b")
            discriminant = 4*(a**3) + 27*(b**2)
            if discriminant != 0:
                with input_row[2]:
                    st.markdown("<div style='padding-top: 25px;'>", unsafe_allow_html=True)
                    st.latex(f"y^2 = x^3 {'+' if a>=0 else ''}{a:.1f}x {'+' if b>=0 else ''}{b:.1f}")
                    st.markdown("</div>", unsafe_allow_html=True)

        # --- Shared Logic for Points ---
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
                else: st.error("Out of domain")
            else:
                yin = st.number_input(f"y{label}", value=1.0, step=0.1, key=f"y_{suffix}")
                roots = np.roots([1, 0, a, (b - yin**2)])
                real_roots = [r.real for r in roots if np.isreal(r)]
                if real_roots:
                    fx = st.selectbox(f"Select x{label}", sorted(real_roots), key=f"sel_{suffix}")
                    fy = yin
            return fx, fy

        # --- Section 2: Point Addition ---
        show_add = False
        with st.expander("Point Addition Calculator", expanded=False):
            col_p, col_q = st.columns(2)
            with col_p: px_add, py_add = get_point_input("P", "add_p", "red", default_x=1.0)
            with col_q: qx_add, qy_add = get_point_input("Q", "add_q", "orange", default_x=0.0)
            if st.button("Calculate P + Q", use_container_width=True):
                show_add = True
                res_add_x, res_add_y, add_slope = add_points(px_add, py_add, qx_add, qy_add, a)
                if res_add_x is not None:
                    st.session_state['add_result'] = (res_add_x, res_add_y, add_slope, px_add, py_add, qx_add, qy_add)
                else: st.error("Point at Infinity")

        # --- Section 3: Scalar Multiplication ---
        show_mult = False
        with st.expander("Scalar Multiplication", expanded=False):
            px_s, py_s = get_point_input("P", "scaler", "blue", default_x=1.0)
            n_val = st.number_input("Multiplier (n)", min_value=1, value=2)
            if st.button(f"Calculate {n_val}P", use_container_width=True):
                show_mult = True
                rx, ry = scalar_mult(n_val, px_s, py_s, a)
                if rx is not None:
                    st.session_state['mult_result'] = (rx, ry, px_s, py_s, n_val)

    with col_right:
        with st.expander("Visualizer", expanded=True):
            plot_range = st.number_input("Plot Range", value=5, key="range")
            fig, ax = plt.subplots(figsize=(6, 5), dpi=150)
            y_m, x_m = np.ogrid[-plot_range:plot_range:500j, -plot_range:plot_range:500j]
            ax.contour(x_m.ravel(), y_m.ravel(), y_m**2 - x_m**3 - a*x_m - b, [0], colors='#3498db')

            # --- Conditional Plotting for Addition ---
            if show_add and 'add_result' in st.session_state:
                rax, ray, rslo, rpx, rpy, rqx, rqy = st.session_state['add_result']
                x_line = np.array([-plot_range, plot_range])
                ax.plot(x_line, rslo*(x_line - rpx) + rpy, color='#9b59b6', linestyle='--', alpha=0.6)
                ax.plot([rax, rax], [-ray, ray], color='grey', linestyle=':', alpha=0.5)
                ax.scatter([rpx, rqx], [rpy, rqy], color=['red', 'orange'], s=50, zorder=5)
                ax.scatter(rax, ray, color='green', s=100, marker='X', zorder=6, label='P+Q')

            # --- Conditional Plotting for Multiplication ---
            if show_mult and 'mult_result' in st.session_state:
                mrx, mry, mpx, mpy, mn = st.session_state['mult_result']
                ax.scatter(mpx, mpy, color='blue', s=50, zorder=5)
                ax.scatter(mrx, mry, color='purple', s=100, marker='D', zorder=6, label=f'{mn}P')

            ax.set_xlim([-plot_range, plot_range]); ax.set_ylim([-plot_range, plot_range])
            ax.grid(True, alpha=0.3); ax.axhline(0, color='grey', alpha=0.2); ax.axvline(0, color='grey', alpha=0.2)
            st.pyplot(fig)
