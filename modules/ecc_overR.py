import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

def run_ecc_overR():    
    st.markdown("""
        <style>
        div[data-testid="stExpander"] details summary {
            background-color: #FDF5E6;
            border-radius: 5px;
            padding: 10px;
        }
        div[data-testid="stExpander"] {
            border: 1px solid #e6e6e6;
            border-radius: 5px;
            background-color: transparent;
        }
        button[data-testid="stNumberInputStepDown"],
        button[data-testid="stNumberInputStepUp"] {
            display: none !important;
        }
        .val-box {
            background-color: #f0f2f6;
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 15px;
            color: black;
            margin-top: 4px;
            text-align: left;
        }
        .small-label {
            font-size: 14px;
            color: #444;
            margin-bottom: 2px;
        }
        </style>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 2])
    
    def add_points(x1, y1, x2, y2, a):
        if x1 is None: return None, None, None
        if x2 is None: return None, None, None
        try:
            if abs(x1 - x2) < 1e-9 and abs(y1 - y2) < 1e-9:
                if abs(y1) < 1e-9: return None, None, None
                s = (3 * x1**2 + a) / (2 * y1)
            elif abs(x1 - x2) < 1e-9:
                return None, None, None
            else:
                s = (y2 - y1) / (x2 - x1)
            xr = s**2 - x1 - x2
            yr = s * (x1 - xr) - y1
            return xr, yr, s 
        except ZeroDivisionError:
            return None, None, None

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

        def get_point_input(label, suffix, color, default_x=1.0):
            st.markdown(f"<span style='color:{color}'>●</span> **Point {label}**", unsafe_allow_html=True)

            if f"mode_{suffix}" not in st.session_state:
                st.session_state[f"mode_{suffix}"] = "X"

            mode = st.session_state[f"mode_{suffix}"]

            r1c1, r1c2, r1c3, r1c4 = st.columns([0.8, 0.4, 0.4, 0.4])
            with r1c1: st.markdown("<div class='small-label' style='padding-top:8px; white-space:nowrap;'>Input mode:</div>", unsafe_allow_html=True)
            with r1c2:
                if st.button("X", key=f"btn_x_{suffix}", use_container_width=True):
                    st.session_state[f"mode_{suffix}"] = "X"
                    st.rerun()
            with r1c3:
                if st.button("Y", key=f"btn_y_{suffix}", use_container_width=True):
                    st.session_state[f"mode_{suffix}"] = "Y"
                    st.rerun()

            fx, fy = None, None
            if mode == "X":
                r2c1, r2c2 = st.columns([1, 3])
                with r2c1:
                    st.markdown(f"<div class='small-label'>x{label}</div>", unsafe_allow_html=True)
                    xin = st.number_input(f"x{label}", value=default_x, step=0.1, key=f"x_{suffix}", label_visibility="collapsed")
                
                rhs = xin**3 + a*xin + b
                if rhs > 0:
                    y_pos = round(math.sqrt(rhs), 6)
                    y_options = [y_pos, -y_pos]
                    with r2c2:
                        inner_col, _ = st.columns([1, 1])
                        with inner_col:
                            st.markdown(f"<div class='small-label'>y{label}</div>", unsafe_allow_html=True)
                            fy = st.selectbox(f"y{label}", y_options, key=f"sel_y_{suffix}", label_visibility="collapsed", format_func=lambda v: f"{v:.2f}")
                    fx = xin
                elif rhs == 0:
                    with r2c2:
                        inner_col, _ = st.columns([1, 1])
                        with inner_col:
                            st.markdown(f"<div class='small-label'>y{label}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='val-box'>0.0000</div>", unsafe_allow_html=True)
                    fx, fy = xin, 0.0
                else:
                    st.error("Out of domain")
            else:
                r2c1, r2c2 = st.columns([1, 3])
                with r2c1:
                    st.markdown(f"<div class='small-label'>y{label}</div>", unsafe_allow_html=True)
                    yin = st.number_input(f"y{label}", value=1.0, step=0.1, key=f"y_{suffix}", label_visibility="collapsed")
                
                roots = np.roots([1, 0, a, (b - yin**2)])
                real_roots = sorted([round(r.real, 6) for r in roots if abs(r.imag) < 1e-6])
                if real_roots:
                    with r2c2:
                        inner_col, _ = st.columns([1, 1])
                        with inner_col:
                            st.markdown(f"<div class='small-label'>x{label}</div>", unsafe_allow_html=True)
                            fx = st.selectbox(f"x{label}", real_roots, key=f"sel_{suffix}", label_visibility="collapsed", format_func=lambda v: f"{v:.2f}")
                    fy = yin

            return fx, fy

        with st.expander("Point Addition", expanded=False):
            col_p, col_q = st.columns(2)
            with col_p: px_add, py_add = get_point_input("P", "add_p", "red", default_x=1.0)
            with col_q: qx_add, qy_add = get_point_input("Q", "add_q", "orange", default_x=0.0)
            
            if px_add is not None and qx_add is not None:
                res_add_x, res_add_y, add_slope = add_points(px_add, py_add, qx_add, qy_add, a)
                if res_add_x is not None:
                    st.latex(f"P + Q = ({res_add_x:.3f},\\ {res_add_y:.3f})")
                    st.session_state['add_result'] = (res_add_x, res_add_y, add_slope, px_add, py_add, qx_add, qy_add)
                else:
                    st.info("Result: Point at Infinity")
                    st.session_state.pop('add_result', None)

        with st.expander("Scalar Multiplication", expanded=False):
            sm_c1, sm_c2, sm_c3 = st.columns([3, 1, 1])
            with sm_c1:
                px_s, py_s = get_point_input("P", "scaler", "blue", default_x=1.0)
            with sm_c2:
                st.empty()
            with sm_c3:
                st.markdown("<div class='small-label'>Multiplier (n)</div>", unsafe_allow_html=True)
                n_val = st.number_input("n", min_value=1, value=2, key="scalar_n", label_visibility="collapsed")

            if px_s is not None:
                rx, ry = scalar_mult(n_val, px_s, py_s, a)
                if rx is not None:
                    st.latex(f"{n_val}P = ({rx:.3f},\\ {ry:.3f})")
                    st.session_state['mult_result'] = (rx, ry, px_s, py_s, n_val)
                else:
                    st.info("Result: Point at Infinity")
                    st.session_state.pop('mult_result', None)

    with col_right:
        with st.expander("Curve Visualization", expanded=False):
            plot_range = st.number_input("Plot Range", value=5, key="range")
            fig, ax = plt.subplots(figsize=(6, 5), dpi=150)
            y_m, x_m = np.ogrid[-plot_range:plot_range:500j, -plot_range:plot_range:500j]
            ax.contour(x_m.ravel(), y_m.ravel(), y_m**2 - x_m**3 - a*x_m - b, [0], colors='#3498db')

            if 'add_result' in st.session_state:
                rax, ray, rslo, rpx, rpy, rqx, rqy = st.session_state['add_result']
                if rslo is not None:
                    x_line = np.array([-plot_range, plot_range])
                    ax.plot(x_line, rslo*(x_line - rpx) + rpy, color='#9b59b6', linestyle='--', alpha=0.6)
                ax.plot([rax, rax], [-ray, ray], color='grey', linestyle=':', alpha=0.5)
                ax.scatter([rpx], [rpy], color='red', s=50, zorder=5)
                ax.annotate('P', xy=(rpx, rpy), xytext=(rpx+0.15, rpy+0.15), fontsize=11, fontweight='bold', color='red')
                ax.scatter([rqx], [rqy], color='orange', s=50, zorder=5)
                ax.annotate('Q', xy=(rqx, rqy), xytext=(rqx+0.15, rqy+0.15), fontsize=11, fontweight='bold', color='orange')
                ax.scatter(rax, ray, color='green', s=100, marker='X', zorder=6)
                ax.annotate('P+Q', xy=(rax, ray), xytext=(rax+0.15, ray+0.15), fontsize=11, fontweight='bold', color='green')

            if 'mult_result' in st.session_state:
                mrx, mry, mpx, mpy, mn = st.session_state['mult_result']
                ax.scatter(mpx, mpy, color='blue', s=50, zorder=5)
                ax.annotate('P', xy=(mpx, mpy), xytext=(mpx+0.15, mpy+0.15), fontsize=11, fontweight='bold', color='blue')
                ax.scatter(mrx, mry, color='purple', s=100, marker='D', zorder=6)
                ax.annotate(f'{mn}P', xy=(mrx, mry), xytext=(mrx+0.15, mry+0.15), fontsize=11, fontweight='bold', color='purple')

            ax.set_xlim([-plot_range, plot_range])
            ax.set_ylim([-plot_range, plot_range])
            ax.grid(True, alpha=0.3)
            ax.axhline(0, color='grey', alpha=0.2)
            ax.axvline(0, color='grey', alpha=0.2)
            st.pyplot(fig)
