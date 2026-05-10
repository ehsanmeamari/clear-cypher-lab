import streamlit as st

# --- 1. MATHEMATICAL FOUNDATION: QUADRATIC FIELD ELEMENTS ---
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
        a, b, c, d, p = self.a, self.b, other.a, other.b, self.p
        real_part = (a * c + b * d * 99) % p
        i_part = (a * d + b * c + 4 * b * d) % p
        return QuadraticFp(real_part, i_part, p)

    def __pow__(self, n):
        result = QuadraticFp(1, 0, self.p)
        base = self
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
        return self.a == other.a and self.b == other.b and self.p == other.p

# --- 2. ELLIPTIC CURVE ARITHMETIC ---
def is_on_curve(P, a, b, p):
    if P is None: return True
    x, y = P
    return (y * y) == (x * x * x + a * x + b)

def point_add(P, Q, a, p):
    if P is None: return Q
    if Q is None: return P
    if P == Q: return point_double(P, a, p)
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2: return None
    slope = (y2 - y1) * (x2 - x1).inverse()
    x3 = (slope * slope - x1 - x2)
    y3 = (slope * (x1 - x3) - y1)
    return (x3, y3)

def point_double(P, a, p):
    if P is None or P[1] == 0: return None
    x, y = P
    slope = (QuadraticFp(3, 0, p) * x * x + a) * (QuadraticFp(2, 0, p) * y).inverse()
    x3 = (slope * slope - QuadraticFp(2, 0, p) * x)
    y3 = (slope * (x - x3) - y)
    return (x3, y3)

# --- 3. MILLER LOOP AND WEIL PAIRING ---
def line_func(P1, P2, Q, a, p):
    if P1 is None or P2 is None or Q is None: return QuadraticFp(1, 0, p)
    x1, y1 = P1
    x2, y2 = P2
    xq, yq = Q
    if x1 != x2:
        l = (y2 - y1) * (x2 - x1).inverse()
        return yq - y1 - l * (xq - x1)
    else:
        if y1 == 0: return xq - x1
        l = (QuadraticFp(3, 0, p) * x1 * x1 + a) * (QuadraticFp(2, 0, p) * y1).inverse()
        return yq - y1 - l * (xq - x1)

def miller_loop(P, Q, n, a, p):
    if P is None or Q is None: return QuadraticFp(1, 0, p)
    t = QuadraticFp(1, 0, p)
    V = P
    for i in range(n.bit_length() - 2, -1, -1):
        S = point_double(V, a, p)
        t = (t * t) * line_func(V, V, Q, a, p) * (line_func(S, (-S[0], -S[1]) if S else None, Q, a, p).inverse())
        V = S
        if (n >> i) & 1:
            S = point_add(V, P, a, p)
            t = t * line_func(V, P, Q, a, p) * (line_func(S, (-S[0], -S[1]) if S else None, Q, a, p).inverse())
            V = S
    return t

def weil_pairing(P, Q, n, a, b, p):
    if P == Q or P is None or Q is None: return QuadraticFp(1, 0, p)
    f_p_q = miller_loop(P, Q, n, a, p)
    f_q_p = miller_loop(Q, P, n, a, p)
    res = f_p_q * f_q_p.inverse()
    if n % 2 == 1: res = -res
    return res

# --- 4. STREAMLIT UI MODULE ---
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
    a = QuadraticFp(1, 0, p)
    b = QuadraticFp(9, 0, p)

    st.markdown("---")

    with st.expander("Protocol Overview", expanded=False):
        st.write("Current Curve Configuration (ZKP Demonstration):")
        st.latex(r"E: y^2 \equiv x^3 + x + 9 \pmod{101}")
        st.info("This module simulates Weil Pairing over extension fields for Zero-Knowledge Proof systems.")

    with st.expander("Pairing Computation", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Point P (Base Domain)")
            st.markdown("<div class='centered-label'>Re(x<sub>P</sub>)</div>", unsafe_allow_html=True)
            xP_r = st.number_input("xP Real", value=25, key="pair_xpr", label_visibility="collapsed")
            st.markdown("<div class='centered-label'>Im(x<sub>P</sub>)</div>", unsafe_allow_html=True)
            xP_i = st.number_input("xP Imag", value=0, key="pair_xpi", label_visibility="collapsed")
            st.markdown("<div class='centered-label'>Re(y<sub>P</sub>)</div>", unsafe_allow_html=True)
            yP_r = st.number_input("yP Real", value=2, key="pair_ypr", label_visibility="collapsed")
            st.markdown("<div class='centered-label'>Im(y<sub>P</sub>)</div>", unsafe_allow_html=True)
            yP_i = st.number_input("yP Imag", value=0, key="pair_ypi", label_visibility="collapsed")
            P = (QuadraticFp(xP_r, xP_i, p), QuadraticFp(yP_r, yP_i, p))

        with col2:
            st.subheader("Point Q (Twist Domain)")
            st.markdown("<div class='centered-label'>Re(x<sub>Q</sub>)</div>", unsafe_allow_html=True)
            xQ_r = st.number_input("xQ Real", value=92, key="pair_xqr", label_visibility="collapsed")
            st.markdown("<div class='centered-label'>Im(x<sub>Q</sub>)</div>", unsafe_allow_html=True)
            xQ_i = st.number_input("xQ Imag", value=53, key="pair_xqi", label_visibility="collapsed")
            st.markdown("<div class='centered-label'>Re(y<sub>Q</sub>)</div>", unsafe_allow_html=True)
            yQ_r = st.number_input("yQ Real", value=6, key="pair_yqr", label_visibility="collapsed")
            st.markdown("<div class='centered-label'>Im(y<sub>Q</sub>)</div>", unsafe_allow_html=True)
            yQ_i = st.number_input("yQ Imag", value=7, key="pair_yqi", label_visibility="collapsed")
            Q = (QuadraticFp(xQ_r, xQ_i, p), QuadraticFp(yQ_r, yQ_i, p))

        st.divider()
        n_val = st.number_input("Torsion Order (n)", value=119, key="torsion_n")

        p_on = is_on_curve(P, a, b, p)
        q_on = is_on_curve(Q, a, b, p)

        if not p_on or not q_on:
            if not p_on:
                st.error("Validation Error: Point P does not lie on the curve $E(\\mathbb{{F}}_{{p^2}})$.")
            if not q_on:
                st.error("Validation Error: Point Q does not lie on the curve $E(\\mathbb{{F}}_{{p^2}})$.")
        else:
            try:
                result = weil_pairing(P, Q, n_val, a, b, p)
                st.success(f"Final Pairing Result: **{result}**")
            except ZeroDivisionError:
                st.warning("Computation Error: Potential linearly dependent points or division by zero in Miller Loop.")

if __name__ == "__main__":
    pairing()
