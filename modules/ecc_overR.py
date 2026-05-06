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
        # Handle point at infinity (identity element)
        if x1 is None:
            return x2, y2, None
        if x2 is None:
            return x1, y1, None
        try:
            if abs(x1 - x2) < 1e-9 and abs(y1 - y2) < 1e-9:
                # Point doubling
                if abs(y1) < 1e-9:
                    return None, None, None  # 2P = infinity when y = 0
                s = (3 * x1**2 + a) / (2 * y1)
            elif abs(x1 - x2) < 1e-9:
                # P + (-P) = infinity
                return None, None, None
            else:
                s = (y2 - y1) / (x2 - x1)
            xr = s**2 - x1 - x2
            yr = s * (x1 - xr) - y1
            return xr, yr, s 
        except ZeroDivisionError:
            return None, None, None

    def scalar_mult(n, px, py, a):
        """
        Double-and-add algorithm for scalar multiplication on ECC.
        None represents the point at infinity (identity element).
        """
        qx, qy = px, py   # current doubling point
        rx, ry = None, None  # accumulator, starts at infinity
        n = int(n)
        while n > 0:
            if n % 2 == 1:
                if rx is None:
                    # R = O + Q = Q
                    rx, ry = qx, qy
                else:
                    res = add_points(rx, ry, qx, qy, a)
                    rx, ry = res[0], res[1]
            # Double Q
            if qx is None:
                break
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

        # Track which section was last updated
        if "last_updated" not in st.session_state:
            st.session_state["last_updated"] = None

        with st.expander("Point Addition", expanded=False):
            if "pa_mode_p" not in st.session_state:
                st.session_state["pa_mode_p"] = "x_to_y"
            if "pa_mode_q" not in st.session_state:
                st.session_state["pa_mode_q"] = "x_to_y"

            h1, h2, h3, h4 = st.columns(4)
            with h1: st.latex("x_P")
            with h2: st.latex("y_P")
            with h3: st.latex("x_Q")
            with h4: st.latex("y_Q")

            # Save previous PA values for change detection
            prev_pa = st.session_state.get("prev_pa_vals", None)

            c1, c2, c3, c4 = st.columns(4)

            xp, yp = None, None
            if st.session_state["pa_mode_p"] == "x_to_y":
                with c1:
                    xp = st.number_input("xP", value=1.0, step=0.1, key="pa_xp", label_visibility="collapsed")
                rhs_p = xp**3 + a*xp + b
                if rhs_p > 0:
                    y_pos_p = round(math.sqrt(rhs_p), 4)
                    with c2:
                        yp = st.selectbox("yP", [y_pos_p, -y_pos_p], key="pa_yp", label_visibility="collapsed", format_func=lambda v: f"{v:.2f}")
                elif rhs_p == 0:
                    with c2:
                        st.markdown("<div class='val-box'>0.00</div>", unsafe_allow_html=True)
                    yp = 0.0
                else:
                    with c2:
                        st.error("∅")
                    xp = None
            else:
                with c2:
                    yp = st.number_input("yP", value=1.0, step=0.1, key="pa_yp2", label_visibility="collapsed")
                roots_p = np.roots([1, 0, a, (b - yp**2)])
                real_p = sorted([round(r.real, 4) for r in roots_p if abs(r.imag) < 1e-6])
                with c1:
                    if real_p:
                        xp = st.selectbox("xP sel", real_p, key="pa_xp_sel", label_visibility="collapsed", format_func=lambda v: f"{v:.2f}")
                    else:
                        st.error("∅")
                        xp = None

            with c1:
                toggle_p = "x→y" if st.session_state["pa_mode_p"] == "x_to_y" else "y→x"
                if st.button(toggle_p, key="pa_toggle_p", use_container_width=True):
                    st.session_state["pa_mode_p"] = "y_to_x" if st.session_state["pa_mode_p"] == "x_to_y" else "x_to_y"
                    st.rerun()

            xq, yq = None, None
            if st.session_state["pa_mode_q"] == "x_to_y":
                with c3:
                    xq = st.number_input("xQ", value=0.0, step=0.1, key="pa_xq", label_visibility="collapsed")
                rhs_q = xq**3 + a*xq + b
                if rhs_q > 0:
                    y_pos_q = round(math.sqrt(rhs_q), 4)
                    with c4:
                        yq = st.selectbox("yQ", [y_pos_q, -y_pos_q], key="pa_yq", label_visibility="collapsed", format_func=lambda v: f"{v:.2f}")
                elif rhs_q == 0:
                    with c4:
                        st.markdown("<div class='val-box'>0.00</div>", unsafe_allow_html=True)
                    yq = 0.0
                else:
                    with c4:
                        st.error("∅")
                    xq = None
            else:
                with c4:
                    yq = st.number_input("yQ", value=1.0, step=0.1, key="pa_yq2", label_visibility="collapsed")
                roots_q = np.roots([1, 0, a, (b - yq**2)])
                real_q = sorted([round(r.real, 4) for r in roots_q if abs(r.imag) < 1e-6])
                with c3:
                    if real_q:
                        xq = st.selectbox("xQ sel", real_q, key="pa_xq_sel", label_visibility="collapsed", format_func=lambda v: f"{v:.2f}")
                    else:
                        st.error("∅")
                        xq = None

            with c3:
                toggle_q = "x→y" if st.session_state["pa_mode_q"] == "x_to_y" else "y→x"
                if st.button(toggle_q, key="pa_toggle_q", use_container_width=True):
                    st.session_state["pa_mode_q"] = "y_to_x" if st.session_state["pa_mode_q"] == "x_to_y" else "x_to_y"
                    st.rerun()

            if xp is not None and xq is not None and yp is not None and yq is not None:
                # Detect if PA inputs changed → mark as last updated
                curr_pa = (xp, yp, xq, yq)
                if prev_pa != curr_pa:
                    st.session_state["prev_pa_vals"] = curr_pa
                    st.session_state["last_updated"] = "pa"

                res_add_x, res_add_y, add_slope = add_points(xp, yp, xq, yq, a)
                if res_add_x is not None:
                    st.info(f"P + Q = ({res_add_x:.2f}, {res_add_y:.2f})")
                    st.session_state['add_result'] = (res_add_x, res_add_y, add_slope, xp, yp, xq, yq)
                else:
                    st.info("Result: Point at Infinity")
                    st.session_state.pop('add_result', None)

        with st.expander("Scalar Multiplication", expanded=False):
            if "sm_mode_p" not in st.session_state:
                st.session_state["sm_mode_p"] = "x_to_y"

            h1, h2, h3, _ = st.columns(4)
            with h1: st.latex("x_P")
            with h2: st.latex("y_P")
            with h3: st.latex("n")

            # Save previous SM values for change detection
            prev_sm = st.session_state.get("prev_sm_vals", None)

            c1, c2, c3, c4 = st.columns(4)

            px_s, py_s = None, None
            if st.session_state["sm_mode_p"] == "x_to_y":
                with c1:
                    px_s = st.number_input("xP_sm", value=1.0, step=0.1, key="sm_xp", label_visibility="collapsed")
                rhs_s = px_s**3 + a*px_s + b
                if rhs_s > 0:
                    y_pos_s = round(math.sqrt(rhs_s), 4)
                    with c2:
                        py_s = st.selectbox("yP_sm", [y_pos_s, -y_pos_s], key="sm_yp", label_visibility="collapsed", format_func=lambda v: f"{v:.2f}")
                elif rhs_s == 0:
                    with c2:
                        st.markdown("<div class='val-box'>0.00</div>", unsafe_allow_html=True)
                    py_s = 0.0
                else:
                    with c2:
                        st.error("∅")
                    px_s = None
            else:
                with c2:
                    py_s = st.number_input("yP_sm2", value=1.0, step=0.1, key="sm_yp2", label_visibility="collapsed")
                roots_s = np.roots([1, 0, a, (b - py_s**2)])
                real_s = sorted([round(r.real, 4) for r in roots_s if abs(r.imag) < 1e-6])
                with c1:
                    if real_s:
                        px_s = st.selectbox("xP_sm sel", real_s, key="sm_xp_sel", label_visibility="collapsed", format_func=lambda v: f"{v:.2f}")
                    else:
                        st.error("∅")
                        px_s = None

            with c1:
                toggle_sm = "x→y" if st.session_state["sm_mode_p"] == "x_to_y" else "y→x"
                if st.button(toggle_sm, key="sm_toggle_p", use_container_width=True):
                    st.session_state["sm_mode_p"] = "y_to_x" if st.session_state["sm_mode_p"] == "x_to_y" else "x_to_y"
                    st.rerun()

            with c3:
                n_val = st.number_input("n_val", min_value=1, value=2, key="scalar_n", label_visibility="collapsed")

            if px_s is not None and py_s is not None:
                # Detect if SM inputs changed → mark as last updated
                curr_sm = (px_s, py_s, n_val)
                if prev_sm != curr_sm:
                    st.session_state["prev_sm_vals"] = curr_sm
                    st.session_state["last_updated"] = "sm"

                rx, ry = scalar_mult(n_val, px_s, py_s, a)
                if rx is not None:
                    st.info(f"{n_val}P = ({rx:.2f}, {ry:.2f})")
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

            if 'add_result' in st.session_state and st.session_state.get("last_updated") == "pa":
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

            if 'mult_result' in st.session_state and st.session_state.get("last_updated") == "sm":
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
