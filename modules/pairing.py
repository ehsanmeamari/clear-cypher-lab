import streamlit as st

# --- 1. MATHEMATICAL FOUNDATION: QUADRATIC FIELD ELEMENTS ---
class QuadraticFp:
    """
    Represents elements in the extension field Fp^2 defined by:
    a + b*i where i^2 = 4i + 99 (Specific to this curve implementation)
    """
    def __init__(self, a, b, p):
        self.p = p
        self.a = a % p  # Real part
        self.b = b % p  # Imaginary/i coefficient

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
        """
        Multiplication over Fp^2 based on i^2 = 4i + 99
        (a+bi)(c+di) = ac + adi + bci + bd(4i+99)
        """
        a, b, c, d, p = self.a, self.b, other.a, other.b, self.p
        real_part = (a * c + b * d * 99) % p
        i_part = (a * d + b * c + 4 * b * d) % p
        return QuadraticFp(real_part, i_part, p)

    def __pow__(self, n):
        """ Binary exponentiation for field elements """
        result = QuadraticFp(1, 0, self.p)
        base = self
        while n > 0:
            if n % 2 == 1: result = result * base
            base = base * base
            n //= 2
        return result

    def inverse(self):
        """
        Computes multiplicative inverse using the norm.
        For i^2 - 4i - 99 = 0, the conjugate of (a+bi) is (a+4b) - bi
        """
        p, a, b = self.p, self.a, self.b
        conj = QuadraticFp(a + 4 * b, -b, p)
        norm = (self * conj).a  # Norm must be a scalar in Fp
        if norm == 0: raise ZeroDivisionError("Element not invertible")
        norm_inv = pow(norm, p - 2, p)
        return QuadraticFp(conj.a * norm_inv, conj.b * norm_inv, p)

    def __eq__(self, other):
        if isinstance(other, int): return self.a == other % self.p and self.b == 0
        return self.a == other.a and self.b == other.b and self.p == other.p

# --- 2. ELLIPTIC CURVE ARITHMETIC ---
def is_on_curve(P, a, b, p):
    """ Verifies if point P satisfies the curve equation y^2 = x^3 + ax + b """
    if P is None: return True
    x, y = P
    return (y * y) == (x * x * x + a * x + b)

def point_add(P, Q, a, p):
    """ Addition of two points on the EC over Fp^2 """
    if P is None: return Q
    if Q is None: return P
    if P == Q: return point_double(P, a, p)
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2: return None # Point at infinity
    
    # Standard addition: slope m = (y2-y1)/(x2-x1)
    slope = (y2 - y1) * (x2 - x1).inverse()
    x3 = (slope * slope - x1 - x2)
    y3 = (slope * (x1 - x3) - y1)
    return (x3, y3)

def point_double(P, a, p):
    """ Doubling a point on the EC (Tangent method) """
    if P is None or P[1] == 0: return None
    x, y = P
    # slope m = (3x^2 + a) / 2y
    slope = (QuadraticFp(3, 0, p) * x * x + a) * (QuadraticFp(2, 0, p) * y).inverse()
    x3 = (slope * slope - QuadraticFp(2, 0, p) * x)
    y3 = (slope * (x - x3) - y)
    return (x3, y3)

# --- 3. MILLER LOOP AND WEIL PAIRING ---
def line_func(P1, P2, Q, a, p):
    """ Evaluates the line function at point Q for Miller's Algorithm """
    if P1 is None or P2 is None or Q is None: return QuadraticFp(1, 0, p)
    x1, y1 = P1
    x2, y2 = P2
    xq, yq = Q
    
    if x1 != x2:
        # Line through two distinct points
        l = (y2 - y1) * (x2 - x1).inverse()
        return yq - y1 - l * (xq - x1)
    else:
        # Vertical tangent or standard doubling tangent
        if y1 == 0: return xq - x1
        l = (QuadraticFp(3, 0, p) * x1 * x1 + a) * (QuadraticFp(2, 0, p) * y1).inverse()
        return yq - y1 - l * (xq - x1)

def miller_loop(P, Q, n, a, p):
    """ Implementation of the Miller Loop for pairing computation """
    if P is None or Q is None: return QuadraticFp(1, 0, p)
    t = QuadraticFp(1, 0, p)
    V = P
    for i in range(n.bit_length() - 2, -1, -1):
        # Double step in Miller's algorithm
        S = point_double(V, a, p)
        t = (t * t) * line_func(V, V, Q, a, p) * (line_func(S, (-S[0], -S[1]) if S else None, Q, a, p).inverse())
        V = S
        if (n >> i) & 1:
            # Addition step in Miller's algorithm
            S = point_add(V, P, a, p)
            t = t * line_func(V, P, Q, a, p) * (line_func(S, (-S[0], -S[1]) if S else None, Q, a, p).inverse())
            V = S
    return t

def weil_pairing(P, Q, n, a, b, p):
    """ Final Weil Pairing calculation: e(P,Q) = (-1)^n * f_P(Q) / f_Q(P) """
    if P == Q or P is None or Q is None: return QuadraticFp(1, 0, p)
    
    f_p_q = miller_loop(P, Q, n, a, p)
    f_q_p = miller_loop(Q, P, n, a, p)
    
    res = f_p_q * f_q_p.inverse()
    if n % 2 == 1: res = -res
    return res

# --- 4. STREAMLIT UI MODULE ---
def pairing():
    """ Renders the Pairing Simulation Lab on Streamlit """
    p = 101
    a = QuadraticFp(1, 0, p)
    b = QuadraticFp(9, 0, p)
    
    st.markdown("---")
    
    with st.expander("Protocol Overview", expanded=True):
        st.write("Current Curve Configuration (Demo Purpose):")
        st.latex(f"E: y^2 \\equiv x^3 + x + 9 \\pmod{{101}}")
        st.info("This lab demonstrates Weil Pairing over extension fields for ZKP systems.")

    # UI Inputs for Points
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Point P (Base Point)")
        xP_r = st.number_input("xP real part", value=25)
        yP_r = st.number_input("yP real part", value=2)
        P = (QuadraticFp(xP_r, 0, p), QuadraticFp(yP_r, 0, p))
        
    with col2:
        st.subheader("Point Q (Twist Point)")
        xQ_r = st.number_input("xQ real part", value=92)
        xQ_i = st.number_input("xQ imaginary part", value=53)
        # Assuming Q y-coordinates are fixed for demo stability
        Q = (QuadraticFp(xQ_r, xQ_i, p), QuadraticFp(6, 7, p))

    n = st.number_input("Order (n-torsion)", value=119)
    method = st.radio("Select Pairing Protocol:", ["Weil Pairing", "Tate Pairing"], horizontal=True)

    if method == "Weil Pairing":
        if not is_on_curve(P, a, b, p) or not is_on_curve(Q, a, b, p):
            st.error("Point Validation Failed: Points must lie on the defined Elliptic Curve.")
        else:
            result = weil_pairing(P, Q, n, a, b, p)
            st.success(f"Final Pairing Result: {result}")
            st.latex(r"e_{Weil}(P, Q) = (-1)^n \cdot \frac{f_P(Q)}{f_Q(P)}")
    else:
        st.info("Tate Pairing module is optimized for high-performance blockchain verification. Coming soon.")

if __name__ == "__main__":
    pairing()
