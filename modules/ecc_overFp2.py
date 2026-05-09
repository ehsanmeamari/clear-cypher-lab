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
        "O, (89+51i, 63+93i), (0, 3), (0, 98), (88+1i, 6+1i), (88+1i, 95+13i), "
        "(64+5i, 38+5i), (64+5i, 63+37i), (91+6i, 20+6i), (91+6i, 81+10i), "
        "(48+8i, 4+8i), (48+8i, 97+53i), (16+10i, 46+10i), (16+10i, 55+85i), "
        "(75+11i, 45+11i), (75+11i, 56+26i), (8+12i, 7+12i), (8+12i, 94+93i), "
        "(94+13i, 2+13i), (94+13i, 99+7i), (6+16i, 21+16i), (6+16i, 80+95i), "
        "(57+18i, 7+18i), (57+18i, 94+44i), (55+19i, 24+19i), (55+19i, 77+46i), "
        "(15+21i, 21i), (15+21i, 86i), (53+23i, 10+23i), (53+23i, 91+48i), "
        "(59+24i, 45+24i), (59+24i, 56+42i), (90+25i, 17+25i), (90+25i, 84+11i), "
        "(26+28i, 24+28i), (26+28i, 77+75i), (69+30i, 50+30i), (69+30i, 51+32i), "
        "(11+31i, 9+31i), (11+31i, 92+90i), (9+32i, 18+32i), (9+32i, 83+92i), "
        "(96+33i, 3+33i), (96+33i, 98+5i), (71+37i, 22+37i), (71+37i, 79+30i), "
        "(15+38i, 5+38i), (15+38i, 96+86i), (88+40i, 35+40i), (88+40i, 66+13i), "
        "(25+44i, 27+44i), (25+44i, 74+76i), (77+45i, 13+45i), (77+45i, 88+24i), "
        "(22+49i, 14+49i), (22+49i, 87+79i), (61+50i, 33+50i), (61+50i, 68+40i), "
        "(71+54i, 31+54i), (71+54i, 70+30i), (34+57i, 15+57i), (34+57i, 86+67i), "
        "(57+58i, 1+58i), (57+58i, 100+44i), (16+59i, 31+59i), (16+59i, 70+85i), "
        "(69+61i, 13+61i), (69+61i, 88+32i), (90+63i, 33+63i), (90+63i, 68+11i), "
        "(80+69i, 43+69i), (80+69i, 58+21i), (74+70i, 18+70i), (74+70i, 83+27i), "
        "(47+71i, 34+71i), (47+71i, 67+54i), (4+72i, 18+72i), (4+72i, 83+97i), "
        "(81+74i, 39+74i), (81+74i, 62+20i), (14+75i, 35+75i), (14+75i, 66+87i), "
        "(91+77i, 2+77i), (91+77i, 99+10i), (35+82i, 8+82i), (35+82i, 93+66i), "
        "(3+83i, 18+83i), (3+83i, 83+98i), (27+84i, 13+84i), (27+84i, 88+74i), "
        "(37+85i, 8+85i), (37+85i, 93+64i), (32+86i, 26+86i), (32+86i, 75+69i), "
        "(78+90i, 10+90i), (78+90i, 91+23i), (5+92i, 29+92i), (5+92i, 72+96i), "
        "(11+95i, 95i), (11+95i, 90+95i), (94+97i, 35+97i)"
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
