import streamlit as st

class QuadraticIFp:
    def __init__(self, a, b, p):
        self.p = p
        self.a = a % p  # real part
        self.b = b % p  # coefficient of i

    def __repr__(self):
        return f"{self.a} + {self.b}i"

    def __add__(self, other):
        return QuadraticIFp(self.a + other.a, self.b + other.b, self.p)

    def __sub__(self, other):
        return QuadraticIFp(self.a - other.a, self.b - other.b, self.p)

    def __neg__(self):
        return QuadraticIFp(-self.a, -self.b, self.p)

    def __mul__(self, other):
        a, b = self.a, self.b
        c, d = other.a, other.b
        p = self.p
        real_part = (a * c + b * d * 99) % p
        i_part = (a * d + b * c + 4 * b * d) % p
        return QuadraticIFp(real_part, i_part, p)

    def __pow__(self, n):
        result = QuadraticIFp(1, 0, self.p)
        base = self
        while n:
            if n & 1:
                result = result * base
            base = base * base
            n >>= 1
        return result

    def inverse(self):
        p = self.p
        a, b = self.a, self.b
        # conjugate
        conj = QuadraticIFp(a + 4 * b, -b, p)
        # norm = x * conjugate (must lie in F_p)
        norm = (self * conj).a 
        if norm == 0:
            raise ZeroDivisionError("Element not invertible")
        norm_inv = pow(norm, p - 2, p)
        return QuadraticIFp(conj.a * norm_inv, conj.b * norm_inv, p)

def extension_math():
    st.subheader("Extension Fields")
    st.write("For this version of our application p=101 and i^2 = 4i + 99 in Extension Fields.")
    
    p = 101

    # --- ROW 1: Addition & Multiplication ---
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        # --- Addition ---
        with st.expander("➕ Addition", expanded=False):
            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                r1 = st.number_input("Real part (a)", value=None, step=1, format="%d", key="r1_add")
            with col2:
                i1 = st.number_input("Imaginary part (a)", value=None, step=1, format="%d", key="i1_add")
            with col3:
                if r1 is not None and i1 is not None:
                    st.markdown("<div style='padding-top: 25px;'>", unsafe_allow_html=True)
                    st.latex(f"a = {r1 % p} + {i1 % p}i")
                    st.markdown("</div>", unsafe_allow_html=True)
            
            st.divider()
            col4, col5, col6 = st.columns([2, 2, 2])
            with col4:
                r2 = st.number_input("Real part (b)", value=None, step=1, format="%d", key="r2_add")
            with col5:
                i2 = st.number_input("Imaginary part (b)", value=None, step=1, format="%d", key="i2_add")
            with col6:
                if r2 is not None and i2 is not None:
                    st.markdown("<div style='padding-top: 25px;'>", unsafe_allow_html=True)
                    st.latex(f"b = {r2 % p} + {i2 % p}i")
                    st.markdown("</div>", unsafe_allow_html=True)

            if all(v is not None for v in [r1, i1, r2, i2]):
                a_obj = QuadraticIFp(r1, i1, p)
                b_obj = QuadraticIFp(r2, i2, p)
                res = a_obj + b_obj
                st.success(f"Result: {res}")
                st.latex(f"({a_obj}) + ({b_obj}) \equiv {res} \pmod{{{p}}}")
            else:
                st.info("Input a & b")

    with row1_col2:
        # --- Multiplication ---
        with st.expander("✖️ Multiplication", expanded=False):
            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                r1_m = st.number_input("Real part (a)", value=None, step=1, format="%d", key="r1_mul")
            with col2:
                i1_m = st.number_input("Imaginary part (a)", value=None, step=1, format="%d", key="i1_mul")
            with col3:
                if r1_m is not None and i1_m is not None:
                    st.markdown("<div style='padding-top: 25px;'>", unsafe_allow_html=True)
                    st.latex(f"a = {r1_m % p} + {i1_m % p}i")
                    st.markdown("</div>", unsafe_allow_html=True)
            
            st.divider()
            col4, col5, col6 = st.columns([2, 2, 2])
            with col4:
                r2_m = st.number_input("Real part (b)", value=None, step=1, format="%d", key="r2_mul")
            with col5:
                i2_m = st.number_input("Imaginary part (b)", value=None, step=1, format="%d", key="i2_mul")
            with col6:
                if r2_m is not None and i2_m is not None:
                    st.markdown("<div style='padding-top: 25px;'>", unsafe_allow_html=True)
                    st.latex(f"b = {r2_m % p} + {i2_m % p}i")
                    st.markdown("</div>", unsafe_allow_html=True)

            if all(v is not None for v in [r1_m, i1_m, r2_m, i2_m]):
                a_obj = QuadraticIFp(r1_m, i1_m, p)
                b_obj = QuadraticIFp(r2_m, i2_m, p)
                res = a_obj * b_obj
                st.success(f"Result: {res}")
                st.latex(f"({a_obj}) \cdot ({b_obj}) \equiv {res} \pmod{{{p}}}")
            else:
                st.info("Input a & b")

    # --- ROW 2: Exponentiation & Inverse ---
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        # --- Exponentiation ---
        with st.expander("🔢 Exponentiation", expanded=False):
            exp = st.number_input("Exponent (n)", value=None, step=1, format="%d", key="exp")
            st.divider()
            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                r1_e = st.number_input("Real part (a)", value=None, step=1, format="%d", key="r1_exp")
            with col2:
                i1_e = st.number_input("Imaginary part (a)", value=None, step=1, format="%d", key="i1_exp")
            with col3:
                if r1_e is not None and i1_e is not None:
                    st.markdown("<div style='padding-top: 25px;'>", unsafe_allow_html=True)
                    st.latex(f"a = {r1_e % p} + {i1_e % p}i")
                    st.markdown("</div>", unsafe_allow_html=True)

            if all(v is not None for v in [r1_e, i1_e, exp]):
                a_obj = QuadraticIFp(r1_e, i1_e, p)
                res = a_obj ** exp
                st.success(f"Result: {res}")
                st.latex(f"({a_obj})^{{{exp}}} \equiv {res} \pmod{{{p}}}")

    with row2_col2:
        # --- Inverse ---
        with st.expander("🔄 Inverse", expanded=False):
            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                r1_v = st.number_input("Real part (a)", value=None, step=1, format="%d", key="r1_inv")
            with col2:
                i1_v = st.number_input("Imaginary part (a)", value=None, step=1, format="%d", key="i1_inv")
            with col3:
                if r1_v is not None and i1_v is not None:
                    st.markdown("<div style='padding-top: 25px;'>", unsafe_allow_html=True)
                    st.latex(f"a = {r1_v % p} + {i1_v % p}i")
                    st.markdown("</div>", unsafe_allow_html=True)

            if r1_v is not None and i1_v is not None:
                a_obj = QuadraticIFp(r1_v, i1_v, p)
                try:
                    res = a_obj.inverse()
                    st.success(f"Result: {res}")
                    st.latex(f"({a_obj})^{{-1}} \equiv {res} \pmod{{{p}}}")
                except ZeroDivisionError:
                    st.error("Not invertible")
