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
    st.write("### 🔢 Addition")
    real1_add = st.number_input("Input the real part for a", value=None, step=1, format="%d", key="r1_add")
    img1_add = st.number_input("Input the imaginary part for a", value=None, step=1, format="%d", key="i1_add")
    a_add = QuadraticIFp(real1_add, img1_add, p) if (real1_add is not None and img1_add is not None) else None
    if a_add: st.latex(f"a={real1_add % p} + {img1_add % p}i")
    
    real2_add = st.number_input("Input the real part for b", value=None, step=1, format="%d", key="r2_add")
    img2_add = st.number_input("Input the imaginary part for b", value=None, step=1, format="%d", key="i2_add")
    b_add = QuadraticIFp(real2_add, img2_add, p) if (real2_add is not None and img2_add is not None) else None
    if b_add: st.latex(f"b={real2_add % p} + {img2_add % p}i")
    
    if a_add is None or b_add is None:
        st.warning("Input the values for Addition")
    else:
        st.success(f"a+b = {a_add + b_add}")

    st.divider()

    # --- Multiplication ---
    st.write("### 🔢 Multiplication")
    real1_mul = st.number_input("Input the real part for a", value=None, step=1, format="%d", key="r1_mul")
    img1_mul = st.number_input("Input the imaginary part for a", value=None, step=1, format="%d", key="i1_mul")
    a_mul = QuadraticIFp(real1_mul, img1_mul, p) if (real1_mul is not None and img1_mul is not None) else None
    if a_mul: st.latex(f"a={real1_mul % p} + {img1_mul % p}i")
    
    real2_mul = st.number_input("Input the real part for b", value=None, step=1, format="%d", key="r2_mul")
    img2_mul = st.number_input("Input the imaginary part for b", value=None, step=1, format="%d", key="i2_mul")
    b_mul = QuadraticIFp(real2_mul, img2_mul, p) if (real2_mul is not None and img2_mul is not None) else None
    if b_mul: st.latex(f"b={real2_mul % p} + {img2_mul % p}i")
    
    if a_mul is None or b_mul is None:
        st.warning("Input the values for Multiplication")
    else:
        st.success(f"a.b = {a_mul * b_mul}")

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
