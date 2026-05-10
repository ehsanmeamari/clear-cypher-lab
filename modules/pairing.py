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

    a = QuadraticFp(1, 0, p)
    b = QuadraticFp(9, 0, p)

    st.markdown("---")

    with st.expander("Protocol Overview", expanded=False):
        st.write("Current Curve Configuration (ZKP Demonstration):")
        st.latex(r"E: y^2 \equiv x^3 + x + 9 \pmod{101}")
        st.info("This module simulates Weil Pairing over extension fields for Zero-Knowledge Proof systems.")

    with st.expander("Pairing Computation (Torsion Order 119)", expanded=True):

        c1, c2, gap, c3, c4, c5, c6 = st.columns([1, 1, 0.3, 1, 1, 1, 1])

        with c1: st.markdown("<div class='centered-label'>x<sub>P</sub></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='centered-label'>y<sub>P</sub></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='centered-label'>Re(x<sub>Q</sub>)</div>", unsafe_allow_html=True)
        with c4: st.markdown("<div class='centered-label'>Im(x<sub>Q</sub>)</div>", unsafe_allow_html=True)
        with c5: st.markdown("<div class='centered-label'>Re(y<sub>Q</sub>)</div>", unsafe_allow_html=True)
        with c6: st.markdown("<div class='centered-label'>Im(y<sub>Q</sub>)</div>", unsafe_allow_html=True)

        c1, c2, gap, c3, c4, c5, c6 = st.columns([1, 1, 0.3, 1, 1, 1, 1])

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
            if not p_on:
                st.error("Validation Error: Point P does not lie on the curve $E(\\mathbb{{F}}_{{101}})$.")
            if not q_on:
                st.error("Validation Error: Point Q does not lie on the curve $E(\\mathbb{{F}}_{{101^2}})$.")
        else:
            try:
                result = weil_pairing(P, Q, int(n_val), a, b)
                st.success(f"Final Pairing Result: **{result}**")
            except ValueError as e:
                st.warning(f"Computation Error: {e}")
            except ZeroDivisionError:
                st.warning("Computation Error: Division by zero in Miller Loop.")

if __name__ == "__main__":
    pairing()
