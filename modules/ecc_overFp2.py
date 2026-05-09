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
        .weil-box {
            background-color: #f0f7ff;
            border-left: 4px solid #3b82f6;
            border-radius: 6px;
            padding: 12px 16px;
            margin: 8px 0;
            font-family: 'Crimson Text', 'Georgia', serif;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 2])

    with col1:
        with st.expander("Curve Definition", expanded=True):
            c1, c2, c3 = st.columns([1, 1, 1])
            with c1: p = st.number_input("Prime (p)", value=101, step=1, min_value=2)
            with c2: a = st.number_input("a", value=1, step=1)
            with c3: b = st.number_input("b", value=9, step=1)

            st.markdown("**Irreducible polynomial:** $x^2 + rx + s$ &nbsp;→&nbsp; $i^2 = Ai + B$")
            c5, c6 = st.columns(2)
            with c5: r_coef = st.number_input("r (coefficient of x)", value=97, step=1)
            with c6: s_coef = st.number_input("s (constant term)", value=2, step=1)

            A = int((-r_coef) % p)
            B = int((-s_coef) % p)

            st.latex(f"y^2 = x^3 + {a}x + {b} \\quad \\text{{over }} \\mathbb{{F}}_{{{p}^2}}")
            st.latex(f"i^2 = {A}i + {B}")

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

        def legendre(n, p):
            if n % p == 0:
                return 0
            return pow(int(n % p), (p - 1) // 2, p) % p

        def count_points_fp1(p, a, b):
            count = 1
            for x in range(p):
                rhs = (pow(x, 3, p) + a * x + b) % p
                L = legendre(rhs, p)
                if L == p - 1:
                    count += 0
                else:
                    count += 1 + L
            return count

        def count_points_fp2_weil(p, a, b):
            N1 = count_points_fp1(p, a, b)
            t  = p + 1 - N1
            N2 = p**2 + 1 - (t**2 - 2 * p)
            return N2, N1, t

        N2, N1, t = count_points_fp2_weil(int(p), int(a), int(b))

        with st.expander(f"Elements on Curve ({N2} points — Weil Theorem)", expanded=True):
            st.warning("For large p (e.g. p=101), finding all points takes time. Use small p for quick results.")
            max_p_auto = st.number_input("Auto-compute if p ≤", value=20, step=1, min_value=2, max_value=50)

            points_fp2 = []
            computed = False

            if p <= max_p_auto:
                for xa in range(p):
                    for xb in range(p):
                        Px = (xa, xb)
                        x2 = fp2_mul(Px, Px); x3 = fp2_mul(x2, Px)
                        ax_ = ((a*xa)%p, (a*xb)%p)
                        rhs = fp2_add(x3, ax_)
                        rhs = fp2_add(rhs, (b%p, 0))
                        for ya in range(p):
                            for yb in range(p):
                                Py = (ya, yb)
                                if fp2_mul(Py, Py) == rhs:
                                    points_fp2.append((Px, Py))
                computed = True
            else:
                if st.button("Compute (may be slow)"):
                    with st.spinner("Computing... please wait"):
                        for xa in range(p):
                            for xb in range(p):
                                Px = (xa, xb)
                                x2 = fp2_mul(Px, Px); x3 = fp2_mul(x2, Px)
                                ax_ = ((a*xa)%p, (a*xb)%p)
                                rhs = fp2_add(x3, ax_)
                                rhs = fp2_add(rhs, (b%p, 0))
                                for ya in range(p):
                                    for yb in range(p):
                                        Py = (ya, yb)
                                        if fp2_mul(Py, Py) == rhs:
                                            points_fp2.append((Px, Py))
                    computed = True

            if computed and points_fp2:
                brute_total = len(points_fp2) + 1
                st.success(f"Total points (including O): {brute_total}")
                if brute_total == N2:
                    st.success(f"✓ Weil formula agrees: {N2}")
                else:
                    st.error(f"⚠ Weil formula gives {N2} — mismatch (check irreducible poly settings)")
                str_pts = ", ".join([f"({fmt(x)}, {fmt(y)})" for x,y in points_fp2])
                st.markdown(f"<div class='math-points'>{{ O, {str_pts} }}</div>", unsafe_allow_html=True)

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
