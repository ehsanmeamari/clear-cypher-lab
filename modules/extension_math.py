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
    st.write("For this version of our application p=101 and i^2 = 4i + 99 in Extension Fields.")
    p = 101

    # --- 1. Addition ---
    with st.expander("➕ Addition", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            real1 = st.number_input("Real part (a)", value=None, step=1, format="%d", key="r1_add")
            img1 = st.number_input("Imaginary part (a)", value=None, step=1, format="%d", key="i1_add")
        with c2:
            real2 = st.number_input("Real part (b)", value=None, step=1, format="%d", key="r2_add")
            img2 = st.number_input("Imaginary part (b)", value=None, step=1, format="%d", key="i2_add")
        
        a = QuadraticIFp(real1, img1, p) if (real1 is not None and img1 is not None) else None
        b = QuadraticIFp(real2, img2, p) if (real2 is not None and img2 is not None) else None
        
        if a and b:
            st.success(f"Result: a + b = {a + b}")
        else:
            st.info("Please input all values for a and b")

    # --- 2. Multiplication ---
    with st.expander("✖️ Multiplication", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            real1 = st.number_input("Real part (a)", value=None, step=1, format="%d", key="r1_mul")
            img1 = st.number_input("Imaginary part (a)", value=None, step=1, format="%d", key="i1_mul")
        with c2:
            real2 = st.number_input("Real part (b)", value=None, step=1, format="%d", key="r2_mul")
            img2 = st.number_input("Imaginary part (b)", value=None, step=1, format="%d", key="i2_mul")
            
        a = QuadraticIFp(real1, img1, p) if (real1 is not None and img1 is not None) else None
        b = QuadraticIFp(real2, img2, p) if (real2 is not None and img2 is not None) else None
        
        if a and b:
            st.success(f"Result: a * b = {a * b}")
        else:
            st.info("Please input all values for a and b")

    # --- 3. Subtraction ---
    with st.expander("➖ Subtraction", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            real1 = st.number_input("Real part (a)", value=None, step=1, format="%d", key="r1_sub")
            img1 = st.number_input("Imaginary part (a)", value=None, step=1, format="%d", key="i1_sub")
        with c2:
            real2 = st.number_input("Real part (b)", value=None, step=1, format="%d", key="r2_sub")
            img2 = st.number_input("Imaginary part (b)", value=None, step=1, format="%d", key="i2_sub")
            
        a = QuadraticIFp(real1, img1, p) if (real1 is not None and img1 is not None) else None
        b = QuadraticIFp(real2, img2, p) if (real2 is not None and img2 is not None) else None
        
        if a and b:
            st.success(f"Result: a - b = {a - b}")
        else:
            st.info("Please input all values for a and b")

    # --- 4. Exponentiation ---
    with st.expander("🔢 Exponentiation", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            real1 = st.number_input("Real part (a)", value=None, step=1, format="%d", key="r1_exp")
            img1 = st.number_input("Imaginary part (a)", value=None, step=1, format="%d", key="i1_exp")
        with c2:
            exp = st.number_input("Exponent (n)", value=None, step=1, format="%d", key="exp_val")
            
        a = QuadraticIFp(real1, img1, p) if (real1 is not None and img1 is not None) else None
        
        if a and exp is not None:
            st.success(f"Result: a^{exp} = {a ** exp}")
        else:
            st.info("Please input base (a) and exponent (n)")

    # --- 5. Inverse ---
    with st.expander("🔄 Inverse", expanded=False):
        real1 = st.number_input("Real part (a)", value=None, step=1, format="%d", key="r1_inv")
        img1 = st.number_input("Imaginary part (a)", value=None, step=1, format="%d", key="i1_inv")
        
        a = QuadraticIFp(real1, img1, p) if (real1 is not None and img1 is not None) else None
        
        if a:
            try:
                st.success(f"Result: a⁻¹ = {a.inverse()}")
            except ZeroDivisionError:
                st.error("Element not invertible")
        else:
            st.info("Please input values for a")
