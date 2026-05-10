import streamlit as st

def ecc_fp2():

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
        .math-points {
            font-family: 'Crimson Text', 'Georgia', serif;
            font-size: 15px;
            line-height: 2;
            word-wrap: break-word;
            overflow-wrap: break-word;
            padding: 8px 4px 16px 4px;
            text-align: left;
        }
        .centered-label {
            text-align: center;
            font-size: 13px;
            font-weight: 500;
            font-family: 'Crimson Text', 'Georgia', serif;
            font-style: italic;
            margin-bottom: 4px;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)

    p = 101
    a = 1
    b = 9
    A = 4
    B = 99

    HARDCODED_POINTS_STR = (
        "O, (0, 3), (0, 98), (1, 27+37i), (1, 74+64i), (2, 25), (2, 76), "
        "(3, 49+26i), (3, 52+75i), (4, 28), (4, 73), (5, 51+25i), (5, 50+76i), "
        "(6, 19+41i), (6, 82+60i), (7, 37), (7, 64), (8, 23), (8, 78), "
        "(9, 79+11i), (9, 22+90i), (10, 3), (10, 98), (11, 51+25i), (11, 50+76i), "
        "(12, 93+4i), (12, 8+97i), (13, 87+7i), (13, 14+94i), (14, 79+11i), "
        "(14, 22+90i), (15, 43+29i), (15, 58+72i), (16, 9), (16, 92), "
        "(17, 9+46i), (17, 92+55i), (18, 1), (18, 100), (19, 25), (19, 76), "
        "(20, 91+5i), (20, 10+96i), (21, 10), (21, 91), (22, 59+21i), (22, 42+80i), "
        "(23, 33), (23, 68), (24, 11), (24, 90), (25, 2), (25, 99), (26, 21), "
        "(26, 80), (27, 23), (27, 78), (28, 89+6i), (28, 12+95i), (29, 77+12i), "
        "(29, 24+89i), (30, 89+6i), (30, 12+95i), (31, 6), (31, 95), (32, 40), "
        "(32, 61), (33, 15), (33, 86), (34, 19), (34, 82), (35, 14), (35, 87), "
        "(36, 49+26i), (36, 52+75i), (37, 87+7i), (37, 14+94i), (38, 50), "
        "(38, 51), (39, 22), (39, 79), (40, 63+19i), (40, 38+82i), (41, 73+14i), "
        "(41, 28+87i), (42, 45), (42, 56), (43, 89+6i), (43, 12+95i), "
        "(44, 17+42i), (44, 84+59i), (45, 28), (45, 73), (46, 85+8i), "
        "(46, 16+93i), (47, 1+50i), (47, 100+51i), (48, 16), (48, 85), "
        "(49, 65+18i), (49, 36+83i)"
    )
    HARDCODED_TOTAL = 10115
    HARDCODED_REMAINING = 10014

    def fp2_mul(X, Y):
        xa, xb = X; ya, yb = Y
        real = (xa*ya + xb*yb*B) % p
        imag = (xa*yb + xb*ya + xb*yb*A) % p
        return (real, imag)

    def fp2_add(X, Y):
        return ((X[0]+Y[0]) % p, (X[1]+Y[1]) % p)

    def fp2_neg(X):
        return ((-X[0]) % p, (-X[1]) % p)

    def fp2_sub(X, Y):
        return fp2_add(X, fp2_neg(Y))

    def fp2_inv(X):
        xa, xb = X
        det = (xa*xa + xa*xb*A - xb*xb*B) % p
        det_inv = pow(int(det), p-2, p)
        ya = ((xa + xb*A) * det_inv) % p
        yb = ((-xb) * det_inv) % p
        return (ya, yb)

    def fp2_is_zero(X):
        return X[0] % p == 0 and X[1] % p == 0

    def is_on_curve_fp2(Px, Py):
        y2 = fp2_mul(Py, Py)
        x2 = fp2_mul(Px, Px)
        x3 = fp2_mul(x2, Px)
        ax = ((a * Px[0]) % p, (a * Px[1]) % p)
        rhs = fp2_add(x3, ax)
        rhs = fp2_add(rhs, (b % p, 0))
        return y2 == rhs

    def point_add_fp2(P, Q):
        if P is None: return Q
        if Q is None: return P
        Px, Py = P; Qx, Qy = Q
        if Px == Qx:
            if Py == fp2_neg(Qy) or (fp2_is_zero(fp2_add(Py, Qy))):
                return None
            if Py == Qy:
                num = fp2_add(fp2_mul((3,0), fp2_mul(Px,Px)), (a%p, 0))
                den = fp2_mul((2,0), Py)
                slope = fp2_mul(num, fp2_inv(den))
            else:
                return None
        else:
            num = fp2_sub(Qy, Py)
            den = fp2_sub(Qx, Px)
            slope = fp2_mul(num, fp2_inv(den))
        x3 = fp2_sub(fp2_sub(fp2_mul(slope, slope), Px), Qx)
        y3 = fp2_sub(fp2_mul(slope, fp2_sub(Px, x3)), Py)
        return (x3, y3)

    def scalar_mul_fp2(k, P):
        res = None; addend = P; k = int(k)
        while k > 0:
            if k & 1: res = point_add_fp2(res, addend)
            addend = point_add_fp2(addend, addend)
            k >>= 1
        return res

    def fmt(x):
        xa, xb = x
        if xb == 0: return str(xa)
        if xa == 0: return f"{xb}i"
        return f"{xa}+{xb}i"

    col1, col2 = st.columns([2, 2])

    with col1:
        with st.expander("Curve Definition", expanded=False):
            st.info("Curve Definition is not available now. The fixed curve is:")
            st.latex(r"y^2 = x^3 + 1 \cdot x + 9 \quad \text{over} \quad \mathbb{F}_{101^2} \quad \text{and} \quad i^2 = 4i + 99")

        with st.expander("Point Addition", expanded=False):
            c1,c2,c3,c4,gap,c5,c6,c7,c8 = st.columns([1,1,1,1,0.4,1,1,1,1])
            with c1: st.markdown("<div class='centered-label'>Re(x<sub>P</sub>)</div>", unsafe_allow_html=True)
            with c2: st.markdown("<div class='centered-label'>Im(x<sub>P</sub>)</div>", unsafe_allow_html=True)
            with c3: st.markdown("<div class='centered-label'>Re(y<sub>P</sub>)</div>", unsafe_allow_html=True)
            with c4: st.markdown("<div class='centered-label'>Im(y<sub>P</sub>)</div>", unsafe_allow_html=True)
            with c5: st.markdown("<div class='centered-label'>Re(x<sub>Q</sub>)</div>", unsafe_allow_html=True)
            with c6: st.markdown("<div class='centered-label'>Im(x<sub>Q</sub>)</div>", unsafe_allow_html=True)
            with c7: st.markdown("<div class='centered-label'>Re(y<sub>Q</sub>)</div>", unsafe_allow_html=True)
            with c8: st.markdown("<div class='centered-label'>Im(y<sub>Q</sub>)</div>", unsafe_allow_html=True)

            c1,c2,c3,c4,gap,c5,c6,c7,c8 = st.columns([1,1,1,1,0.4,1,1,1,1])
            with c1: xPa = st.number_input("xPa", value=0, key="xPa", label_visibility="collapsed")
            with c2: xPb = st.number_input("xPb", value=0, key="xPb", label_visibility="collapsed")
            with c3: yPa = st.number_input("yPa", value=3, key="yPa", label_visibility="collapsed")
            with c4: yPb = st.number_input("yPb", value=0, key="yPb", label_visibility="collapsed")
            with c5: xQa = st.number_input("xQa", value=0, key="xQa", label_visibility="collapsed")
            with c6: xQb = st.number_input("xQb", value=0, key="xQb", label_visibility="collapsed")
            with c7: yQa = st.number_input("yQa", value=3, key="yQa", label_visibility="collapsed")
            with c8: yQb = st.number_input("yQb", value=0, key="yQb", label_visibility="collapsed")

            PA = ((int(xPa)%p, int(xPb)%p), (int(yPa)%p, int(yPb)%p))
            QA = ((int(xQa)%p, int(xQb)%p), (int(yQa)%p, int(yQb)%p))

            p_on = is_on_curve_fp2(*PA)
            q_on = is_on_curve_fp2(*QA)

            if p_on and q_on:
                R_add = point_add_fp2(PA, QA)
                if R_add:
                    st.latex(f"P + Q = ({fmt(R_add[0])},\\ {fmt(R_add[1])})")
                else:
                    st.latex("P + Q = \\mathcal{O}")
            else:
                if not p_on: st.warning("P is NOT on the curve!")
                if not q_on: st.warning("Q is NOT on the curve!")

        with st.expander("Scalar Multiplication", expanded=False):
            c1,c2,c3,c4,c5 = st.columns(5)
            with c1: st.markdown("<div class='centered-label'>n</div>", unsafe_allow_html=True)
            with c2: st.markdown("<div class='centered-label'>Re(x<sub>P</sub>)</div>", unsafe_allow_html=True)
            with c3: st.markdown("<div class='centered-label'>Im(x<sub>P</sub>)</div>", unsafe_allow_html=True)
            with c4: st.markdown("<div class='centered-label'>Re(y<sub>P</sub>)</div>", unsafe_allow_html=True)
            with c5: st.markdown("<div class='centered-label'>Im(y<sub>P</sub>)</div>", unsafe_allow_html=True)

            c1,c2,c3,c4,c5 = st.columns(5)
            with c1: n_val = st.number_input("n", value=2, min_value=1, key="n_sm", label_visibility="collapsed")
            with c2: xSa = st.number_input("xSa", value=0, key="xSa", label_visibility="collapsed")
            with c3: xSb = st.number_input("xSb", value=0, key="xSb", label_visibility="collapsed")
            with c4: ySa = st.number_input("ySa", value=3, key="ySa", label_visibility="collapsed")
            with c5: ySb = st.number_input("ySb", value=0, key="ySb", label_visibility="collapsed")

            PS = ((int(xSa)%p, int(xSb)%p), (int(ySa)%p, int(ySb)%p))
            if is_on_curve_fp2(*PS):
                R_mul = scalar_mul_fp2(n_val, PS)
                if R_mul:
                    st.latex(f"{n_val}P = ({fmt(R_mul[0])},\\ {fmt(R_mul[1])})")
                else:
                    st.latex(f"{n_val}P = \\mathcal{{O}}")
            else:
                st.warning("P is NOT on the curve!")

    with col2:
        with st.expander("Check if a Point is on the Curve", expanded=False):
            
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.markdown("<div class='centered-label'>Re(x)</div>", unsafe_allow_html=True)
            with c2: st.markdown("<div class='centered-label'>Im(x)</div>", unsafe_allow_html=True)
            with c3: st.markdown("<div class='centered-label'>Re(y)</div>", unsafe_allow_html=True)
            with c4: st.markdown("<div class='centered-label'>Im(y)</div>", unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns(4)
            with c1: chk_xa = st.number_input("Re(x)", value=0, key="chk_xa", label_visibility="collapsed")
            with c2: chk_xb = st.number_input("Im(x)", value=0, key="chk_xb", label_visibility="collapsed")
            with c3: chk_ya = st.number_input("Re(y)", value=3, key="chk_ya", label_visibility="collapsed")
            with c4: chk_yb = st.number_input("Im(y)", value=0, key="chk_yb", label_visibility="collapsed")

            Px_chk = (int(chk_xa) % p, int(chk_xb) % p)
            Py_chk = (int(chk_ya) % p, int(chk_yb) % p)

            if is_on_curve_fp2(Px_chk, Py_chk):
                st.success(f"✓ The point ({fmt(Px_chk)}, {fmt(Py_chk)}) is on the curve $E(\mathbb{F}_{101^2})$.")
            else:
                st.error(f"✗ The point ({fmt(Px_chk)}, {fmt(Py_chk)}) is NOT on the curve $E(\mathbb{F}_{101^2})$.")

        st.latex(r"\mathbb{F}_{101^2}")
                
        with st.expander(f"Elements on Curve ({HARDCODED_TOTAL} points — Weil Theorem)", expanded=False):
            st.markdown(
                f"<div class='math-points'>{{ {HARDCODED_POINTS_STR}, "
                f"... ({HARDCODED_REMAINING} more points not shown) }}</div>",
                unsafe_allow_html=True
            )
            st.warning(
                "For large p (e.g. p=101), finding all points takes time. "
                "As an example, we listed up to 100 points below and skip the rest."
            )
