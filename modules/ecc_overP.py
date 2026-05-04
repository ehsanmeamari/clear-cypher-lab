import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def ecc_fp():
    st.set_page_config(layout="wide")
    
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital@0;1&display=swap');
        div[data-testid="stExpander"] details summary {
            background-color: #FDF5E6; 
            border-radius: 8px 8px 0px 0px;
            padding: 10px;
        }
        div[data-testid="stExpander"] {
            background-color: transparent !important;
            border: 1px solid #e6e6e6;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        input:disabled {
            -webkit-text-fill-color: black !important;
            color: black !important;
            opacity: 1 !important;
            background: #f0f2f6 !important;
        }
        div[data-testid="stWidgetLabel"] label p, 
        div[data-testid="stWidgetLabel"] p,
        .st-emotion-cache-16ids9d p {
            color: black !important;
            opacity: 1 !important;
            font-weight: 500;
        }
        div[data-testid="stTextInput"] label p {
            color: black !important;
            opacity: 1 !important;
        }
        .math-points {
            font-family: 'Crimson Text', 'Georgia', serif;
            font-size: 16px;
            line-height: 2;
            word-wrap: break-word;
            overflow-wrap: break-word;
            padding: 8px 4px 16px 4px;
            text-align: left;
        }
        </style>
    """, unsafe_allow_html=True)

    points_list = []
    col1, col2 = st.columns([2, 2])

    with col1:
        with st.expander("Curve Definition", expanded=False):
            c1, c2, c3, c4 = st.columns([1, 1, 1, 2.5])            
            with c1: p = st.number_input("Prime (p)", value=17, step=1)
            with c2: a = st.number_input("Parameter (a)", value=2, step=1)
            with c3: b = st.number_input("Parameter (b)", value=13, step=1)

            discriminant = (4*(a**3) + 27*(b**2)) % p
            if discriminant != 0:
                with c4:
                    st.markdown("<div style='margin-top: 25px;'>", unsafe_allow_html=True)
                    st.latex(f"E: y^2 \\equiv x^3 + {a % p}x + {b % p} \\pmod{{{p}}}")
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("Singular Curve!")

        if discriminant != 0:
            for x in range(p):
                for y in range(p):
                    if (y**2 - (x**3 + a*x + b)) % p == 0:
                        points_list.append((x, y))

        if points_list:
            with st.expander(f"Points on curve ({len(points_list)+1} points):", expanded=False):
                str_points = ", ".join([f"({pt[0]},{pt[1]})" for pt in points_list])
                st.markdown(f"<div class='math-points'>{{ 𝒪, {str_points} }}</div>", unsafe_allow_html=True)

        st.divider()

        sub_col1, sub_col2 = st.columns(2)

        with sub_col1:
            with st.expander("Point Addition", expanded=True):
                c1, c2, c3, c4 = st.columns(4)
                with c1: xP = st.number_input("xP", value=0, key="xP")
                with c2: yP = st.number_input("yP", value=8, key="yP")
                with c3: xQ = st.number_input("xQ", value=0, key="xQ")
                with c4: yQ = st.number_input("yQ", value=9, key="yQ")

                P = (xP % p, yP % p)
                Q = (xQ % p, yQ % p)
                R_add = None

                p_on = is_on_curve(P, a, b, p)
                q_on = is_on_curve(Q, a, b, p)

                if p_on and q_on:
                    R_add = point_add(P, Q, a, p)
                    xR_val = str(R_add[0]) if R_add else "\\infty"
                    yR_val = str(R_add[1]) if R_add else "\\infty"
                    st.latex(f"({xP}, {yP}) + ({xQ}, {yQ}) = ({xR_val}, {yR_val})")
                else:
                    st.warning("One or both points are NOT on the curve!")

        with sub_col2:
            with st.expander("Scalar Multiplication", expanded=True):
                c1, c2, c3 = st.columns(3)
                with c1: n_val = st.number_input("n", value=3, key="n_s")
                with c2: xPs = st.number_input("xP", value=0, key="xP_s")
                with c3: yPs = st.number_input("yP", value=8, key="yP_s")

                Ps = (xPs % p, yPs % p)
                Rs_mul = None
                if is_on_curve(Ps, a, b, p):
                    Rs_mul = scalar_mul(n_val, Ps, a, p)
                    xR_val = str(Rs_mul[0]) if Rs_mul else "\\infty"
                    yR_val = str(Rs_mul[1]) if Rs_mul else "\\infty"
                    st.latex(f"{n_val} \\times ({xPs}, {yPs}) = ({xR_val}, {yR_val})")

    with col2:
        with st.expander("Curve Visualization", expanded=True):
            if points_list:
                fig, ax = plt.subplots(figsize=(6, 6))
                px, py = zip(*points_list)
                ax.scatter(px, py, facecolors='none', edgecolors='#3498db', s=50, label='Curve Points', linewidth=1.5)
                
                if is_on_curve(P, a, b, p):
                    ax.scatter(P[0], P[1], color='#f1c40f', s=100, label='P', zorder=5)
                if is_on_curve(Q, a, b, p):
                    ax.scatter(Q[0], Q[1], color='#e74c3c', s=100, label='Q', zorder=5)
                if R_add:
                    ax.scatter(R_add[0], R_add[1], color='#2ecc71', s=150, marker='X', label='P+Q', zorder=6)

                ax.set_title(f"Points on Elliptic Curve over F_{p}", fontsize=12)
                ax.xaxis.set_major_locator(MaxNLocator(nbins=5, integer=True))
                ax.yaxis.set_major_locator(MaxNLocator(nbins=5, integer=True))
                ax.set_xlim(-0.5, p - 0.5)
                ax.set_ylim(-0.5, p - 0.5)
                ax.grid(True, linestyle='--', alpha=0.6)
                ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
                st.pyplot(fig)

def mod_inv(n, p): return pow(n % p, p - 2, p)
def is_on_curve(P, a, b, p):
    if P is None: return True
    return (P[1]**2 - (P[0]**3 + a*P[0] + b)) % p == 0

def point_add(P, Q, a, p):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P; x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0: return None
    if x1 == x2 and y1 == y2:
        if y1 == 0: return None
        slope = ((3 * x1**2 + a) * mod_inv(2 * y1, p)) % p
    else:
        slope = ((y2 - y1) * mod_inv(x2 - x1, p)) % p
    x3 = (slope**2 - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    return (x3, y3)

def scalar_mul(k, P, a, p):
    res = None; addend = P; k = int(k)
    while k > 0:
        if k & 1: res = point_add(res, addend, a, p)
        addend = point_add(addend, addend, a, p)
        k >>= 1
    return res

if __name__ == "__main__":
    ecc_fp()
