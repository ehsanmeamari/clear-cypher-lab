import streamlit as st

def mod_inv(n, p):
    """Compute modular inverse using Fermat's Little Theorem."""
    return pow(n, p - 2, p)

def is_on_curve(P, a, b, p):
    """Check whether a point lies on the curve."""
    if P is None:
        return True
    x, y = P
    # Fixed Syntax: Use * for multiplication
    return (y * y - (x**3 + a * x + b)) % p == 0

def point_neg(P, p):
    """Compute -P on elliptic curve over F_p."""
    if P is None:
        return None
    x, y = P
    return (x, (-y) % p)

def point_double(P, a, p):
    """Double a point P on elliptic curve over F_p."""
    if P is None:
        return None
    x, y = P
    if y == 0:
        return None
    # Fixed Syntax: Added * operators
    slope = ((3 * x * x + a) * mod_inv(2 * y, p)) % p
    x3 = (slope * slope - 2 * x) % p
    y3 = (slope * (x - x3) - y) % p
    return (x3, y3)

def point_add(P, Q, a, p):
    """Add two points P and Q on elliptic curve over F_p."""
    if P is None: return Q
    if Q is None: return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and (y1 % p != y2 % p):
        return None

    if P == Q:
        return point_double(P, a, p)

    # Fixed Syntax: Added * operator
    slope = ((y2 - y1) * mod_inv(x2 - x1, p)) % p
    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    return (x3, y3)

def scalar_mul(k, P, a, p):
    """Compute k * P using double-and-add."""
    if k == 0 or P is None:
        return None
    if k < 0:
        return scalar_mul(-k, point_neg(P, p), a, p)

    result = None
    addend = P
    while k:
        if k & 1:
            result = point_add(result, addend, a, p)
        addend = point_double(addend, a, p)
        k >>= 1
    return result

def ecc_fp():
    st.subheader("Finite Field Fp")
    
    # --- Curve Parameters ---
    col1, col2, col3 = st.columns(3)
    with col1:
        p = st.number_input("p", value=None, step=1, format="%d")
    with col2:
        a = st.number_input("a", value=None, step=1, format="%d")
    with col3:
        b = st.number_input("b", value=None, step=1, format="%d")

    if a is None or b is None or p is None:
        st.latex(r"y^2=x^3+ax+b \pmod{p}")
    else:
        if a == 0: st.latex(f"y^2 = x^3 + {b} \pmod{{{p}}}")
        elif b == 0: st.latex(f"y^2 = x^3 + {a}x \pmod{{{p}}}")
        else: st.latex(f"y^2 = x^3 + {a}x + {b} \pmod{{{p}}}")

        # --- Operations ---
        op = st.radio("Operations:", ["P + Q", "Scalar multiplication (kP)"], horizontal=True)

        if op == "P + Q":
            c1, c2 = st.columns(2)
            with c1:
                x1 = st.number_input("x of P", value=None, step=1, format="%d")
                y1 = st.number_input("y of P", value=None, step=1, format="%d")
            with c2:
                x2 = st.number_input("x of Q", value=None, step=1, format="%d")
                y2 = st.number_input("y of Q", value=None, step=1, format="%d")

            P = (x1, y1) if x1 is not None and y1 is not None else None
            Q = (x2, y2) if x2 is not None and y2 is not None else None

            if P and Q:
                if not is_on_curve(P, a, b, p): st.error("Point P is not on the curve.")
                elif not is_on_curve(Q, a, b, p): st.error("Point Q is not on the curve.")
                else:
                    R = point_add(P, Q, a, p)
                    st.success(f"Result P + Q = {R if R else 'Infinity'}")

        elif op == "Scalar multiplication (kP)":
            c1, c2 = st.columns(2)
            with c1:
                x1 = st.number_input("x-coordinate", value=None, step=1, format="%d")
                y1 = st.number_input("y-coordinate", value=None, step=1, format="%d")
            with c2:
                k = st.number_input("Integer k", value=1, step=1, format="%d")

            P = (x1, y1) if x1 is not None and y1 is not None else None
            if P:
                if not is_on_curve(P, a, b, p): st.error("Point P is not on the curve.")
                else:
                    R = scalar_mul(k, P, a, p)
                    st.success(f"Result {k}P = {R if R else 'Infinity'}")
