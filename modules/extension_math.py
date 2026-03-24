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
    st.write("For this version of our application p=101 and i^2 = 4i + 99 in Extension Fields. We will extend it for all cases soon.")
    
    op = st.radio("Operations:", ["Addition", "Multiplication", "Subtraction", "Exponentiation", "Inverse"], horizontal=True)
    p = 101

    if op == "Addition":
        st.write("### 🔢 Addition")
        real1 = st.number_input("Input the real part for a", value=None, step=1, format="%d", key="r1_add")
        img1 = st.number_input("Input the imaginary part for a", value=None, step=1, format="%d", key="i1_add")
        a = QuadraticIFp(real1, img1, p) if (real1 is not None and img1 is not None) else None
        if a: st.latex(f"a={real1 % p} + {img1 % p}i")
        
        real2 = st.number_input("Input the real part for b", value=None, step=1, format="%d", key="r2_add")
        img2 = st.number_input("Input the imaginary part for b", value=None, step=1, format="%d", key="i2_add")
        b = QuadraticIFp(real2, img2, p) if (real2 is not None and img2 is not None) else None
        if b: st.latex(f"b={real2 % p} + {img2 % p}i")
        
        if a is None or b is None:
            st.warning("Input the values for all")
        else:
            st.success(f"a+b = {a + b}")

    elif op == "Multiplication":
        st.write("### 🔢 Multiplication")
        real1 = st.number_input("Input the real part for a", value=None, step=1, format="%d", key="r1_mul")
        img1 = st.number_input("Input the imaginary part for a", value=None, step=1, format="%d", key="i1_mul")
        a = QuadraticIFp(real1, img1, p) if (real1 is not None and img1 is not None) else None
        if a: st.latex(f"a={real1 % p} + {img1 % p}i")
        
        real2 = st.number_input("Input the real part for b", value=None, step=1, format="%d", key="r2_mul")
        img2 = st.number_input("Input the imaginary part for b", value=None, step=1, format="%d", key="i2_mul")
        b = QuadraticIFp(real2, img2, p) if (real2 is not None and img2 is not None) else None
        if b: st.latex(f"b={real2 % p} + {img2 % p}i")
        
        if a is None or b is None:
            st.warning("Input the values for all")
        else:
            st.success(f"a.b = {a * b}")

    elif op == "Subtraction":
        st.write("### 🔢 Subtraction")
        real1 = st.number_input("Input the real part for a", value=None, step=1, format="%d", key="r1_sub")
        img1 = st.number_input("Input the imaginary part for a", value=None, step=1, format="%d", key="i1_sub")
        a = QuadraticIFp(real1, img1, p) if (real1 is not None and img1 is not None) else None
        if a: st.latex(f"a={real1 % p} + {img1 % p}i")
        
        real2 = st.number_input("Input the real part for b", value=None, step=1, format="%d", key="r2_sub")
        img2 = st.number_input("Input the imaginary part for b", value=None, step=1, format="%d", key="i2_sub")
        b = QuadraticIFp(real2, img2, p) if (real2 is not None and img2 is not None) else None
        if b: st.latex(f"b={real2 % p} + {img2 % p}i")
        
        if a is None or b is None:
            st.warning("Input the values for all")
        else:
            st.success(f"a-b = {a - b}")

    elif op == "Exponentiation":
        st.write("### 🔢 Exponentiation")
        exp = st.number_input("Input the exponent", value=None, step=1, format="%d", key="exp")
        real1 = st.number_input("Input the real part for a", value=None, step=1, format="%d", key="r1_exp")
        img1 = st.number_input("Input the imaginary part for a", value=None, step=1, format="%d", key="i1_exp")
        a = QuadraticIFp(real1, img1, p) if (real1 is not None and img1 is not None) else None
        if a: st.latex(f"a={real1 % p} + {img1 % p}i")
        
        if a is None or exp is None:
            st.warning("Input the values for all")
        else:
            st.success(rf"a^{{{exp}}} = {a ** exp}")

    elif op == "Inverse":
        st.write("### 🔢 Inverse")
        real1 = st.number_input("Input the real part for a", value=None, step=1, format="%d", key="r1_inv")
        img1 = st.number_input("Input the imaginary part for a", value=None, step=1, format="%d", key="i1_inv")
        a = QuadraticIFp(real1, img1, p) if (real1 is not None and img1 is not None) else None
        if a: st.latex(f"a={real1 % p} + {img1 % p}i")
        
        if a is None:
            st.warning("Input the values for all")
        else:
            try:
                st.success(f"The inverse of a is {a.inverse()}")
            except ZeroDivisionError:
                st.error("Element not invertible")
