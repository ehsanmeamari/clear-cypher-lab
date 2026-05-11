import streamlit as st

p = 101

class QuadraticFp:
    def __init__(self, a, b, p):
        self.p = p
        self.a = a % p
        self.b = b % p

    def __repr__(self):
        if self.a == 0 and self.b == 0: return "0"
        if self.b == 0: return f"{self.a}"
        if self.a == 0: return f"{self.b}i"
        return f"{self.a} + {self.b}i"

    def __add__(self, other):
        return QuadraticFp(self.a + other.a, self.b + other.b, self.p)

    def __sub__(self, other):
        return QuadraticFp(self.a - other.a, self.b - other.b, self.p)

    def __neg__(self):
        return QuadraticFp(-self.a, -self.b, self.p)

    def __mul__(self, other):
        if isinstance(other, int):
            return QuadraticFp(self.a * other, self.b * other, self.p)
        a, b, c, d, p = self.a, self.b, other.a, other.b, self.p
        real_part = (a * c + b * d * 99) % p
        i_part = (a * d + b * c + 4 * b * d) % p
        return QuadraticFp(real_part, i_part, p)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, n):
        if n == 0: return QuadraticFp(1, 0, self.p)
        if n < 0: return self.inverse().__pow__(-n)
        result = QuadraticFp(1, 0, self.p)
        base = QuadraticFp(self.a, self.b, self.p)
        while n > 0:
            if n % 2 == 1: result = result * base
            base = base * base
            n //= 2
        return result

    def inverse(self):
        p, a, b = self.p, self.a, self.b
        conj = QuadraticFp(a + 4 * b, -b, p)
        norm = (self * conj).a
        if norm == 0: raise ZeroDivisionError("Element not invertible")
        norm_inv = pow(norm, p - 2, p)
        return QuadraticFp(conj.a * norm_inv, conj.b * norm_inv, p)

    def __eq__(self, other):
        if isinstance(other, int): return self.a == other % self.p and self.b == 0
        if not isinstance(other, QuadraticFp): return False
        return self.a == other.a and self.b == other.b and self.p == other.p

    def __hash__(self):
        return hash((self.a, self.b, self.p))


ONE_EL = QuadraticFp(1, 0, p)
TWO    = QuadraticFp(2, 0, p)
THREE  = QuadraticFp(3, 0, p)

def is_on_curve(P, a, b):
    if P is None: return True
    x, y = P
    return (y * y) == (x * x * x + a * x + b)

def point_neg(P):
    if P is None: return None
    return (P[0], -P[1])

def point_double(P, a):
    if P is None: return None
    x, y = P
    if y == QuadraticFp(0, 0, p): return None
    slope = (THREE * x * x + a) * (TWO * y).inverse()
    x3 = slope * slope - TWO * x
    y3 = slope * (x - x3) - y
    return (x3, y3)

def point_add(P, Q, a):
    if P is None: return Q
    if Q is None: return P
    if P == Q: return point_double(P, a)
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2: return None
    slope = (y2 - y1) * (x2 - x1).inverse()
    x3 = slope * slope - x1 - x2
    y3 = slope * (x1 - x3) - y1
    return (x3, y3)

def scalar_mul(n, P, a):
    if n == 0 or P is None: return None
    if n < 0:
        n = -n
        P = point_neg(P)
    result = None
    addend = P
    while n > 0:
        if n & 1: result = point_add(result, addend, a)
        addend = point_double(addend, a)
        n >>= 1
    return result

def line(T, R, Q, a):
    if Q is None:
        raise ValueError("Q must not be infinity.")
    if T is None and R is None:
        return ONE_EL
    if T is None:
        return Q[0] - R[0]
    if R is None:
        return Q[0] - T[0]
    if T != R:
        if T[0] == R[0]:
            return Q[0] - T[0]
        else:
            l = (R[1] - T[1]) * (R[0] - T[0]).inverse()
            return Q[1] - T[1] - l * (Q[0] - T[0])
    else:
        numerator = THREE * T[0] * T[0] + a
        denominator = TWO * T[1]
        if denominator == QuadraticFp(0, 0, p):
            return Q[0] - T[0]
        else:
            l = numerator * denominator.inverse()
            return Q[1] - T[1] - l * (Q[0] - T[0])

def miller(P, Q, n, a):
    if Q is None:
        raise ValueError("Q must not be infinity.")
    if n == 0:
        raise ValueError("n must be nonzero.")
    n_is_negative = False
    if n < 0:
        n = -n
        n_is_negative = True
    t = ONE_EL
    V = P
    bitt_n = bin(n)[2:]
    nbin = [int(bitt_n[-i]) for i in range(1, n.bit_length() + 1)]
    i = len(nbin) - 2
    while i > -1:
        S = point_double(V, a)
        ell = line(V, V, Q, a)
        vee = line(S, point_neg(S), Q, a)
        t = (t ** 2) * (ell * vee.inverse())
        V = S
        if nbin[i] == 1:
            S = point_add(V, P, a)
            ell = line(V, P, Q, a)
            vee = line(S, point_neg(S), Q, a)
            t = t * ell * vee.inverse()
            V = S
        i -= 1
    if n_is_negative:
        vee = line(V, point_neg(V), Q, a)
        t = (t * vee).inverse()
    return t

def weil_pairing(P, Q, n, a, b):
    if not is_on_curve(Q, a, b):
        raise ValueError("Q is not on the curve.")
    if scalar_mul(n, P, a) is not None or scalar_mul(n, Q, a) is not None:
        raise ValueError("Points must both be n-torsion.")
    if P == Q or P is None or Q is None:
        return ONE_EL
    try:
        last_bit = n % 2
        deno = miller(Q, P, n, a)
        res = QuadraticFp(-1, 0, p) ** last_bit * (miller(P, Q, n, a) * deno.inverse())
        return res
    except ZeroDivisionError:
        return ONE_EL

def pairing():
    st.markdown("""
        <style>
        div[data-testid="stExpander"] details summary {
            background-color: #FDF5E6;
            border-radius: 8px 8px 0px 0px;
            padding: 10px;
            font-weight: bold;
        }
        div[data-testid="stExpander"] {
            background-color: transparent !important;
            border: 1px solid #e6e6e6;
            border-radius: 8px;
            margin-bottom: 10px;
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
        .math-points {
            font-family: 'Crimson Text', 'Georgia', serif;
            font-size: 15px;
            line-height: 2;
            word-wrap: break-word;
            overflow-wrap: break-word;
            padding: 8px 4px 16px 4px;
            text-align: left;
        }
        </style>
    """, unsafe_allow_html=True)

    a_int = 1
    b_int = 9
    a = QuadraticFp(a_int, 0, p)
    b = QuadraticFp(b_int, 0, p)

    fp1_points = []
    for x in range(p):
        for y in range(p):
            if (y*y - (x*x*x + a_int*x + b_int)) % p == 0:
                fp1_points.append((x, y))

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

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("Curve Definition", expanded=False):
            st.latex(r"E: y^2 \equiv x^3 + x + 9 \pmod{101}, \quad i^2 = 4i + 99 \quad \text{(irreducible polynomial over } \mathbb{F}_{101}\text{)}")

        str_points = ", ".join([f"({pt[0]},{pt[1]})" for pt in fp1_points])
        with st.expander(f"Points on Curve E(F₁₀₁) ({len(fp1_points)+1} points)", expanded=False):
            st.markdown(
                f"<div class='math-points'>{{ 𝒪, {str_points} }}</div>",
                unsafe_allow_html=True
            )

    with col2:
        with st.expander(f"Elements on Curve E(F₁₀₁²) ({HARDCODED_TOTAL} points — Weil Theorem)", expanded=False):
            st.markdown(
                f"<div class='math-points'>{{ {HARDCODED_POINTS_STR}, "
                f"... ({HARDCODED_REMAINING} more points not shown) }}</div>",
                unsafe_allow_html=True
            )
            st.warning(
                "For large p (e.g. p=101), finding all points takes time. "
                "As an example, we listed up to 100 points below and skip the rest."
            )

    with st.expander("Pairing Computation (Torsion Order = 119)", expanded=True):

        c1, c2, gap, c3, c4, c5, c6, gap, c7 = st.columns([1, 1, 0.3, 1, 1, 1, 1, 0.3, 4])

        with c1: st.markdown("<div class='centered-label'>x<sub>P</sub></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='centered-label'>y<sub>P</sub></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='centered-label'>Re(x<sub>Q</sub>)</div>", unsafe_allow_html=True)
        with c4: st.markdown("<div class='centered-label'>Im(x<sub>Q</sub>)</div>", unsafe_allow_html=True)
        with c5: st.markdown("<div class='centered-label'>Re(y<sub>Q</sub>)</div>", unsafe_allow_html=True)
        with c6: st.markdown("<div class='centered-label'>Im(y<sub>Q</sub>)</div>", unsafe_allow_html=True)
        with c7: st.empty()

        c1, c2, gap, c3, c4, c5, c6, gap, c7 = st.columns([1, 1, 0.3, 1, 1, 1, 1, 0.3, 4])

        with c1: xP_r = st.number_input("xP", value=19, key="pair_xpr", label_visibility="collapsed")
        with c2: yP_r = st.number_input("yP", value=25, key="pair_ypr", label_visibility="collapsed")
        with c3: xQ_r = st.number_input("xQ Real", value=89, key="pair_xqr", label_visibility="collapsed")
        with c4: xQ_i = st.number_input("xQ Imag", value=51, key="pair_xqi", label_visibility="collapsed")
        with c5: yQ_r = st.number_input("yQ Real", value=63, key="pair_yqr", label_visibility="collapsed")
        with c6: yQ_i = st.number_input("yQ Imag", value=93, key="pair_yqi", label_visibility="collapsed")

        P = (QuadraticFp(int(xP_r), 0, p), QuadraticFp(int(yP_r), 0, p))
        Q = (QuadraticFp(int(xQ_r), int(xQ_i), p), QuadraticFp(int(yQ_r), int(yQ_i), p))

        n_val = 119
        p_on = is_on_curve(P, a, b)
        q_on = is_on_curve(Q, a, b)

        if not p_on or not q_on:
            with c7:
                if not p_on:
                    st.error("P not on curve.")
                if not q_on:
                    st.error("Q not on curve.")
        else:
            try:
                result = weil_pairing(P, Q, int(n_val), a, b)
                with c7:
                    st.markdown("""
                        <style>
                        div[data-testid="stExpander"] .stLatex {
                            background-color: #d4edda;
                            border-radius: 8px;
                            padding: 4px 8px;
                        }
                        </style>
                    """, unsafe_allow_html=True)
                    st.latex(
                        rf"e\!\left(({int(xP_r)},\,{int(yP_r)}),\;"
                        rf"({int(xQ_r)}+{int(xQ_i)}i,\;"
                        rf"{int(yQ_r)}+{int(yQ_i)}i)\right)"
                        rf"= {result.a} + {result.b}i"
                    )
            except ValueError as e:
                with c7:
                    if "n-torsion" in str(e):
                        st.warning("Point is on the curve but not of order 119. Please choose an n-torsion point.")
                    else:
                        st.warning(f"Error: {e}")
            except ZeroDivisionError:
                with c7:
                    st.warning("Division by zero.")

if __name__ == "__main__":
    pairing()
