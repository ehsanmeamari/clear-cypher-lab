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
            font-size: 20px;
            font-weight: 500;
            font-family: 'Crimson Text', 'Georgia', serif;
            font-style: italic;
            margin-bottom: 4px;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)

    # ── parameters of the curve ─────────────────────────────────────────────
    p = 101
    a = 1
    b = 9
    A = 4
    B = 99

    # ── hardcode list of 100 elements ──────────────────────────────────────
    HARDCODED_POINTS_STR = (
        "O, (51i+89, 93i+63), (0, 3), (0, 98), (1i, 88i+6), (1i, 13i+95), "
        "(5i, 64i+38), (5i, 37i+63), (6i, 91i+20), (6i, 10i+81), "
        "(8i, 48i+4), (8i, 53i+97), (10i, 16i+46), (10i, 85i+55), "
        "(11i, 75i+45), (11i, 26i+56), (12i, 8i+7), (12i, 93i+94), "
        "(13i, 94i+2), (13i, 7i+99), (16i, 6i+21), (16i, 95i+80), "
        "(18i, 57i+7), (18i, 44i+94), (19i, 55i+24), (19i, 46i+77), "
        "(21i, 15i), (21i, 86i), (23i, 53i+10), (23i, 48i+91), "
        "(24i, 59i+45), (24i, 42i+56), (25i, 90i+17), (25i, 11i+84), "
        "(28i, 26i+24), (28i, 75i+77), (30i, 69i+50), (30i, 32i+51), "
        "(31i, 11i+9), (31i, 90i+92), (32i, 9i+18), (32i, 92i+83), "
        "(33i, 96i+3), (33i, 5i+98), (37i, 71i+22), (37i, 30i+79), "
        "(38i, 15i+5), (38i, 86i+96), (40i, 88i+35), (40i, 13i+66), "
        "(44i, 25i+27), (44i, 76i+74), (45i, 77i+13), (45i, 24i+88), "
        "(49i, 22i+14), (49i, 79i+87), (50i, 61i+33), (50i, 40i+68), "
        "(54i, 71i+31), (54i, 30i+70), (57i, 34i+15), (57i, 67i+86), "
        "(58i, 57i+1), (58i, 44i+100), (59i, 16i+31), (59i, 85i+70), "
        "(61i, 69i+13), (61i, 32i+88), (63i, 90i+33), (63i, 11i+68), "
        "(69i, 80i+43), (69i, 21i+58), (70i, 74i+18), (70i, 27i+83), "
        "(71i, 47i+34), (71i, 54i+67), (72i, 4i+18), (72i, 97i+83), "
        "(74i, 81i+39), (74i, 20i+62), (75i, 14i+35), (75i, 87i+66), "
        "(77i, 91i+2), (77i, 10i+99), (82i, 35i+8), (82i, 66i+93), "
        "(83i, 3i+18), (83i, 98i+83), (84i, 27i+13), (84i, 74i+88), "
        "(85i, 37i+8), (85i, 64i+93), (86i, 32i+26), (86i, 69i+75), "
        "(90i, 78i+10), (90i, 23i+91), (92i, 5i+29), (92i, 96i+72), "
        "(95i, 11), (95i, 90), (97i, 94i+35)"
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
        return f"{xb}i+{xa}"

    col1, col2 = st.columns([2, 2])

    with col1:
        with st.expander("Curve Definition", expanded=True):
            st.info("Curve Definition is not available now. The fixed curve is:")
            st.latex(r"y^2 = x^3 + 1 \cdot x + 9 \quad \text{over } \mathbb{F}_{101^2}")
            st.latex(r"i^2 = 4i + 99")

        with st.expander(f"Elements on Curve ({HARDCODED_TOTAL} points — Weil Theorem)", expanded=True):
            st.warning(
                "For large p (e.g. p=101), finding all points takes time. "
                "As an example, we list up to 100 points below and skip the rest."
            )
            st.markdown(
                f"<div class='math-points'>{{ {HARDCODED_POINTS_STR}, "
                f"... ({HARDCODED_REMAINING} more points not shown) }}</div>",
                unsafe_allow_html=True
            )

        with st.expander("Check if a Point is on the Curve", expanded=True):
            st.markdown("Enter the coordinates of a point to check if it belongs to the curve.")

            c1, c2, c3, c4 = st.columns(4)
            with c1: st.markdown("<div class='centered-label'>Re(x)</div>", unsafe_allow_html=True)
            with c2: st.markdown("<div class='centered-label'>Im(x)</div>", unsafe_allow_html=True)
            with c3: st.markdown("<div class='centered-label'>Re(y)</div>", unsafe_allow_html=True)
            with c4: st.markdown("<div class='centered-label'>Im(y)</div>", unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns(4)
            with c1: chk_xa = st.number_input("Re(x)", value=89, key="chk_xa", label_visibility="collapsed")
            with c2: chk_xb = st.number_input("Im(x)", value=51, key="chk_xb", label_visibility="collapsed")
            with c3: chk_ya = st.number_input("Re(y)", value=63, key="chk_ya", label_visibility="collapsed")
            with c4: chk_yb = st.number_input("Im(y)", value=93, key="chk_yb", label_visibility="collapsed")

            Px_chk = (int(chk_xa) % p, int(chk_xb) % p)
            Py_chk = (int(chk_ya) % p, int(chk_yb) % p)

            if is_on_curve_fp2(Px_chk, Py_chk):
                st.success(f"✓ The point ({fmt(Px_chk)}, {fmt(Py_chk)}) is on the curve E(𝔽_p²).")
            else:
                st.error(f"✗ The point ({fmt(Px_chk)}, {fmt(Py_chk)}) is NOT on the curve.")

    with col2:
        with st.expander("Point Addition", expanded=True):
            c1,c2,c3,c4,c5,c6,c7,c8 = st.columns(8)
            with c1: st.markdown("<div class='centered-label'>Re(x<sub>P</sub>)</div>", unsafe_allow_html=True)
            with c2: st.markdown("<div class='centered-label'>Im(x<sub>P</sub>)</div>", unsafe_allow_html=True)
            with c3: st.markdown("<div class='centered-label'>Re(y<sub>P</sub>)</div>", unsafe_allow_html=True)
            with c4: st.markdown("<div class='centered-label'>Im(y<sub>P</sub>)</div>", unsafe_allow_html=True)
            with c5: st.markdown("<div class='centered-label'>Re(x<sub>Q</sub>)</div>", unsafe_allow_html=True)
            with c6: st.markdown("<div class='centered-label'>Im(x<sub>Q</sub>)</div>", unsafe_allow_html=True)
            with c7: st.markdown("<div class='centered-label'>Re(y<sub>Q</sub>)</div>", unsafe_allow_html=True)
            with c8: st.markdown("<div class='centered-label'>Im(y<sub>Q</sub>)</div>", unsafe_allow_html=True)

            c1,c2,c3,c4,c5,c6,c7,c8 = st.columns(8)
            with c1: xPa = st.number_input("xPa", value=89, key="xPa", label_visibility="collapsed")
            with c2: xPb = st.number_input("xPb", value=51, key="xPb", label_visibility="collapsed")
            with c3: yPa = st.number_input("yPa", value=63, key="yPa", label_visibility="collapsed")
            with c4: yPb = st.number_input("yPb", value=93, key="yPb", label_visibility="collapsed")
            with c5: xQa = st.number_input("xQa", value=89, key="xQa", label_visibility="collapsed")
            with c6: xQb = st.number_input("xQb", value=51, key="xQb", label_visibility="collapsed")
            with c7: yQa = st.number_input("yQa", value=63, key="yQa", label_visibility="collapsed")
            with c8: yQb = st.number_input("yQb", value=93, key="yQb", label_visibility="collapsed")

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

        with st.expander("Scalar Multiplication", expanded=True):
            c1,c2,c3,c4,c5 = st.columns(5)
            with c1: st.markdown("<div class='centered-label'>n</div>", unsafe_allow_html=True)
            with c2: st.markdown("<div class='centered-label'>Re(x<sub>P</sub>)</div>", unsafe_allow_html=True)
            with c3: st.markdown("<div class='centered-label'>Im(x<sub>P</sub>)</div>", unsafe_allow_html=True)
            with c4: st.markdown("<div class='centered-label'>Re(y<sub>P</sub>)</div>", unsafe_allow_html=True)
            with c5: st.markdown("<div class='centered-label'>Im(y<sub>P</sub>)</div>", unsafe_allow_html=True)

            c1,c2,c3,c4,c5 = st.columns(5)
            with c1: n_val = st.number_input("n", value=2, min_value=1, key="n_sm", label_visibility="collapsed")
            with c2: xSa = st.number_input("xSa", value=89, key="xSa", label_visibility="collapsed")
            with c3: xSb = st.number_input("xSb", value=51, key="xSb", label_visibility="collapsed")
            with c4: ySa = st.number_input("ySa", value=63, key="ySa", label_visibility="collapsed")
            with c5: ySb = st.number_input("ySb", value=93, key="ySb", label_visibility="collapsed")

            PS = ((int(xSa)%p, int(xSb)%p), (int(ySa)%p, int(ySb)%p))
            if is_on_curve_fp2(*PS):
                R_mul = scalar_mul_fp2(n_val, PS)
                if R_mul:
                    st.latex(f"{n_val}P = ({fmt(R_mul[0])},\\ {fmt(R_mul[1])})")
                else:
                    st.latex(f"{n_val}P = \\mathcal{{O}}")
            else:
                st.warning("P is NOT on the curve!")
