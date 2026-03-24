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

def extension_math2():
    st.subheader("Extension Fields")
    st.write("For this version of our application p=101 and i^2 = 4i + 99 in Extension Fields. We will extend it for all cases soon.")
    
    p = 101

    # --- Addition ---
    with st.expander("🔢 Addition", expanded=False):
        # --- Row for Input 'a' ---
        col1, col2, col3 = st.columns([2, 2, 2]) # Three equal columns
        with col1:
            r1 = st.number_input("Real part (a)", value=None, step=1, format="%d", key="r1_add")
        with col2:
            i1 = st.number_input("Imaginary part (a)", value=None, step=1, format="%d", key="i1_add")
        with col3:
            # Display 'a' in the same row
            if r1 is not None and i1 is not None:
                st.markdown("<div style='padding-top: 25px;'>", unsafe_allow_html=True) # Align with inputs
                st.latex(f"a = {r1 % p} + {i1 % p}i")
                st.markdown("</div>", unsafe_allow_html=True)
        
        st.divider()

        # --- Row for Input 'b' ---
        col4, col5, col6 = st.columns([2, 2, 2])
        with col4:
            r2 = st.number_input("Real part (b)", value=None, step=1, format="%d", key="r2_add")
        with col5:
            i2 = st.number_input("Imaginary part (b)", value=None, step=1, format="%d", key="i2_add")
        with col6:
            # Display 'b' in the same row
            if r2 is not None and i2 is not None:
                st.markdown("<div style='padding-top: 25px;'>", unsafe_allow_html=True)
                st.latex(f"b = {r2 % p} + {i2 % p}i")
                st.markdown("</div>", unsafe_allow_html=True)

        # --- Result ---
        if all(v is not None for v in [r1, i1, r2, i2]):
            a_obj = QuadraticIFp(r1, i1, p)
            b_obj = QuadraticIFp(r2, i2, p)
            result_add = a_obj + b_obj
            st.latex(f"({a_obj}) + ({b_obj}) \equiv {result_add} \pmod{{{p}}}")
        else:
            st.warning("Please input all values for Addition")

    st.divider()

    # --- Multiplication ---
    with st.expander("✖️ Multiplication", expanded=False):
        # --- Row for Input 'a' ---
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            r1_mul = st.number_input("Real part (a)", value=None, step=1, format="%d", key="r1_mul")
        with col2:
            i1_mul = st.number_input("Imaginary part (a)", value=None, step=1, format="%d", key="i1_mul")
        with col3:
            # Display 'a' in the same row
            if r1_mul is not None and i1_mul is not None:
                st.markdown("<div style='padding-top: 25px;'>", unsafe_allow_html=True)
                st.latex(f"a = {r1_mul % p} + {i1_mul % p}i")
                st.markdown("</div>", unsafe_allow_html=True)
        
        st.divider()

        # --- Row for Input 'b' ---
        col4, col5, col6 = st.columns([2, 2, 2])
        with col4:
            r2_mul = st.number_input("Real part (b)", value=None, step=1, format="%d", key="r2_mul")
        with col5:
            i2_mul = st.number_input("Imaginary part (b)", value=None, step=1, format="%d", key="i2_mul")
        with col6:
            # Display 'b' in the same row
            if r2_mul is not None and i2_mul is not None:
                st.markdown("<div style='padding-top: 25px;'>", unsafe_allow_html=True)
                st.latex(f"b = {r2_mul % p} + {i2_mul % p}i")
                st.markdown("</div>", unsafe_allow_html=True)

        # --- Result ---
        if all(v is not None for v in [r1_mul, i1_mul, r2_mul, i2_mul]):
            a_mul_obj = QuadraticIFp(r1_mul, i1_mul, p)
            b_mul_obj = QuadraticIFp(r2_mul, i2_mul, p)
            result_mul = a_mul_obj * b_mul_obj
            st.latex(f"({a_mul_obj}) \cdot ({b_mul_obj}) \equiv {result_mul} \pmod{{{p}}}")
        else:
            st.warning("Please input all values for Multiplication")

    st.divider()

    # --- Subtraction ---
    st.write("### 🔢 Subtraction")
    real1_sub = st.number_input("Input the real part for a", value=None, step=1, format="%d", key="r1_sub")
    img1_sub = st.number_input("Input the imaginary part for a", value=None, step=1, format="%d", key="i1_sub")
    a_sub = QuadraticIFp(real1_sub, img1_sub, p) if (real1_sub is not None and img1_sub is not None) else None
    if a_sub: st.latex(f"a={real1_sub % p} + {img1_sub % p}i")
    
    real2_sub = st.number_input("Input the real part for b", value=None, step=1, format="%d", key="r2_sub")
    img2_sub = st.number_input("Input the imaginary part for b", value=None, step=1, format="%d", key="i2_sub")
    b_sub = QuadraticIFp(real2_sub, img2_sub, p) if (real2_sub is not None and img2_sub is not None) else None
    if b_sub: st.latex(f"b={real2_sub % p} + {img2_sub % p}i")
    
    if a_sub is None or b_sub is None:
        st.warning("Input the values for Subtraction")
    else:
        st.success(f"a-b = {a_sub - b_sub}")

    st.divider()

    # --- Exponentiation ---
    st.write("### 🔢 Exponentiation")
    exp = st.number_input("Input the exponent", value=None, step=1, format="%d", key="exp")
    real1_exp = st.number_input("Input the real part for a", value=None, step=1, format="%d", key="r1_exp")
    img1_exp = st.number_input("Input the imaginary part for a", value=None, step=1, format="%d", key="i1_exp")
    a_exp = QuadraticIFp(real1_exp, img1_exp, p) if (real1_exp is not None and img1_exp is not None) else None
    if a_exp: st.latex(f"a={real1_exp % p} + {img1_exp % p}i")
    
    if a_exp is None or exp is None:
        st.warning("Input the values for Exponentiation")
    else:
        st.success(rf"a^{{{exp}}} = {a_exp ** exp}")

    st.divider()

    # --- Inverse ---
    st.write("### 🔢 Inverse")
    real1_inv = st.number_input("Input the real part for a", value=None, step=1, format="%d", key="r1_inv")
    img1_inv = st.number_input("Input the imaginary part for a", value=None, step=1, format="%d", key="i1_inv")
    a_inv = QuadraticIFp(real1_inv, img1_inv, p) if (real1_inv is not None and img1_inv is not None) else None
    if a_inv: st.latex(f"a={real1_inv % p} + {img1_inv % p}i")
    
    if a_inv is None:
        st.warning("Input the values for Inverse")
    else:
        try:
            st.success(f"The inverse of a is {a_inv.inverse()}")
        except ZeroDivisionError:
            st.error("Element not invertible")
