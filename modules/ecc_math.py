import streamlit as st
import matplotlib.pyplot as plt

def ecc_fp():
    """
    Renders the Elliptic Curve Cryptography tool over Finite Fields (Fp).
    """
    
    # Inject Custom CSS for Cream Headers and Transparent Content area
    st.markdown("""
        <style>
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
        div[data-testid="stExpander"] details > div[role="region"] {
            background-color: transparent !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # State variables
    points_list = []
    
    col1, col2 = st.columns([8, 5])

    with col1:
        # --- Section: Curve Definition ---
        with st.expander("Curve Definition", expanded=True):
            c1, c2, c3, c4 = st.columns([1, 1, 1, 2.5])            
            with c1: p = st.number_input("Prime (p)", value=17, step=1)
            with c2: a = st.number_input("Parameter (a)", value=2, step=1)
            with c3: b = st.number_input("Parameter (b)", value=13, step=1)

            discriminant = (4*(a**3) + 27*(b**2)) % p
            with c4:
                if discriminant == 0:
                    st.error("Singular Curve!")
                else:
                    st.markdown("<div style='margin-top: 25px;'>", unsafe_allow_html=True)
                    st.latex(f"E: y^2 \\equiv x^3 + {a % p}x + {b % p} \\pmod{{{p}}}")
                    st.markdown("</div>", unsafe_allow_html=True)

        # Calculation of points
        for x in range(p):
            for y in range(p):
                if (y**2 - (x**3 + a*x + b)) % p == 0:
                    points_list.append((x, y))

        # --- Section: Point Addition ---
        with st.expander("Point Addition", expanded=True):
            st.write("**Enter Coordinates for P and Q:**")
            cols_add = st.columns([0.4, 1, 0.2, 1, 0.4, 0.6, 0.4, 1, 0.2, 1, 0.4, 0.6, 0.4, 1, 0.2, 1, 0.4])
            sym = "<div style='text-align: center; font-size: 20px; font-weight: bold; line-height: 45px;'>"
        
            with cols_add[0]: st.markdown(f"{sym}(</div>", unsafe_allow_html=True)
            with cols_add[1]: xP = st.number_input("xP", value=0, key="xP")
            with cols_add[2]: st.markdown(f"{sym},</div>", unsafe_allow_html=True)
            with cols_add[3]: yP = st.number_input("yP", value=8, key="yP")
            with cols_add[4]: st.markdown(f"{sym})</div>", unsafe_allow_html=True)
            with cols_add[5]: st.markdown(f"{sym}+</div>", unsafe_allow_html=True)
            with cols_add[6]: st.markdown(f"{sym}(</div>", unsafe_allow_html=True)
            with cols_add[7]: xQ = st.number_input("xQ", value=0, key="xQ")
            with cols_add[8]: st.markdown(f"{sym},</div>", unsafe_allow_html=True)
            with cols_add[9]: yQ = st.number_input("yQ", value=9, key="yQ")
            with cols_add[10]: st.markdown(f"{sym})</div>", unsafe_allow_html=True)
            with cols_add[11]: st.markdown(f"{sym}=</div>", unsafe_allow_html=True)

            P = (xP % p, yP % p)
            Q = (xQ % p, yQ % p)
            
            if is_on_curve(P, a, b, p) and is_on_curve(Q, a, b, p):
                R = point_add(P, Q, a, p)
                with cols_add[12]: st.markdown(f"{sym}(</div>", unsafe_allow_html=True)
                with cols_add[13]: st.text_input("xR", value=str(R[0]) if R else "∞", disabled=True, key="res_x_add")
                with cols_add[14]: st.markdown(f"{sym},</div>", unsafe_allow_html=True)
                with cols_add[15]: st.text_input("yR", value=str(R[1]) if R else "∞", disabled=True, key="res_y_add")
                with cols_add[16]: st.markdown(f"{sym})</div>", unsafe_allow_html=True)
                if R is None: st.caption("Result: Point at infinity $\mathcal{O}$")
            else:
                st.warning("One of the points is not on the curve.")

        # --- Section: Scalar Multiplication ---
        with st.expander("Scalar Multiplication (nP)", expanded=True):
            st.write("**Enter Scalar n and Point P:**")
            cols_mul = st.columns([1, 0.4, 0.4, 1, 0.2, 1, 0.2, 0.3, 0.2, 1.2, 0.2, 1.2, 0.2])

            with cols_mul[0]: n_val = st.number_input("n", value=3, key="n_scalar")
            with cols_mul[1]: st.markdown(f"{sym}×</div>", unsafe_allow_html=True)
            with cols_mul[2]: st.markdown(f"{sym}(</div>", unsafe_allow_html=True)
            with cols_mul[3]: xPs = st.number_input("xP", value=0, key="xP_s")
            with cols_mul[4]: st.markdown(f"{sym},</div>", unsafe_allow_html=True)
            with cols_mul[5]: yPs = st.number_input("yP", value=8, key="yP_s")
            with cols_mul[6]: st.markdown(f"{sym})</div>", unsafe_allow_html=True)
            with cols_mul[7]: st.markdown(f"{sym}=</div>", unsafe_allow_html=True)

            Ps = (xPs % p, yPs % p)
            if is_on_curve(Ps, a, b, p):
                Rs = scalar_mul(n_val, Ps, a, p)
                with cols_mul[8]: st.markdown(f"{sym}(</div>", unsafe_allow_html=True)
                with cols_mul[9]: st.text_input("xR", value=str(Rs[0]) if Rs else "∞", disabled=True, key="res_x_mul")
                with cols_mul[10]: st.markdown(f"{sym},</div>", unsafe_allow_html=True)
                with cols_mul[11]: st.text_input("yR", value=str(Rs[1]) if Rs else "∞", disabled=True, key="res_y_mul")
                with cols_mul[12]: st.markdown(f"{sym})</div>", unsafe_allow_html=True)
            else:
                st.warning("Point P is not on the curve.")

# --- Mathematical Helper Functions ---
def mod_inv(n, p):
    return pow(n % p, p - 2, p)

def is_on_curve(P, a, b, p):
    if P is None: return True
    x, y = P
    return (y**2 - (x**3 + a*x + b)) % p == 0

def point_add(P, Q, a, p):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0: return None
    if x1 == x2 and y1 == y2:
        slope = ((3 * x1**2 + a) * mod_inv(2 * y1, p)) % p
    else:
        slope = ((y2 - y1) * mod_inv(x2 - x1, p)) % p
    x3 = (slope**2 - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    return (x3, y3)

def scalar_mul(k, P, a, p):
    result = None
    addend = P
    k = int(k)
    while k > 0:
        if k & 1: result = point_add(result, addend, a, p)
        addend = point_add(addend, addend, a, p)
        k >>= 1
    return result

if __name__ == "__main__":
    ecc_fp()
