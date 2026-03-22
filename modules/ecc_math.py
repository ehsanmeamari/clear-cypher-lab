import streamlit as st
def ecc_fp():
    #st.subheader("عملیات بر روی منحنی‌های محدود (Fp)")
    st.subheader("Finite Field Fp")
    # ---------- پارامترهای منحنی ----------
    col1, col2, col3 = st.columns(3)
    with col1:
        p = st.number_input("p", value=None, step=1, format="%d")
    with col2:
        a = st.number_input("a", value=None, step=1, format="%d")
    with col3:
        b = st.number_input("b", value=None, step=1, format="%d")
    if a==None or b==None:
        st.latex(r"y^2=x^3+ax+b")
    elif a==0:
        st.latex(f"y^2 = x^3 + {b}")
    elif b==0:
        st.latex(f"y^2 = x^3 + {a}x")
    else:
        st.latex(f"y^2 = x^3 + {a}x+{b}")
    # ---------- operations ----------
    op = st.radio("Operations:", ["P + Q", "Scaler multiplication(kP)"], horizontal=True)
    if op == "P + Q":
        # ---------- input points ----------
        #st.markdown("P=")
        x1 = st.number_input("Input the x-coordinate of P", value=None, step=1, format="%d")
        y1 = st.number_input("Input the y-coordinate of P", value=None, step=1, format="%d")
        P = (x1, y1) if x1 and y1 else None
        if x1!= None and y1!=None:
            st.latex(f"P=({x1}, {y1})")
        if is_on_curve(P, a, b, p)==False:
                st.error("The point P is not on the curve.")
        x2 = st.number_input("Input the x-coordinate of Q", value=None, step=1, format="%d")
        y2 = st.number_input("Input the y-coordinate of Q", value=None, step=1, format="%d")
        Q = (x2, y2) if x2 and y2 else None
        if x2!= None and y2!= None:
            st.latex(f"Q=({x2}, {y2})")
        if is_on_curve(Q, a, b, p)==False:
                st.error("The point Q is not on the curve.")
        if P is None or Q is None:
            st.warning("Input the values for all")
        else:
            if not is_on_curve(P, a, b, p) or not is_on_curve(Q, a, b, p):
                st.error("Edit the points. One or both points are not on the curve.")
            else:
                R = point_add(P, Q, a, p)
                if R==None:
                    st.success(f"P+Q = {"Infinity"}");
                else:
                    st.success(f"P+Q = {R}");
    elif op=="Scaler multiplication(kP)":
        # ---------- input points ----------
        x1 = st.number_input("Input the x-coordinate", value=None, step=1, format="%d")
        y1 = st.number_input("Input the y-coordinate", value=None, step=1, format="%d")
        P = (x1, y1) if x1 and y1 else None
        if x1!= None and y1!=None:
            st.latex(f"P=({x1}, {y1})")
        k = st.number_input("Input the integer k", value=0, step=1, format="%d")
        if P is None or k is None:
            st.warning("input the values for all")
        else:
            if not is_on_curve(P, a, b, p):
                st.error("The point P is not on the curve.")
            else:
                R = scalar_mul(k, P, a, p)
                if R==None:
                    st.success(f"kP = {"Infinity"}");
                else:
                    st.success(f"kP = {R}");
    # showing other notes
    #st.caption("Note: The NONE shows the infinity point foe the elliptic curve")
#st.caption("Note: The NONE shows the infinity point foe the elliptic curve")
def mod_inv(n, p):
    return pow(n, p - 2, p)

def is_on_curve(P, a, b, p):
    """Check whether a point lies on the curve."""
    if P is None:
        return True
    x, y = P
    return (y  y - (x  x  x + a  x + b)) % p == 0
def point_neg(P, p):
    """
    Compute -P on elliptic curve over F_p.
    """
    if P is None:
        return None
    x, y = P
    return (x, (-y) % p)
def scalar_mul(k, P, a, p):
    """
    Compute k  P using double-and-add.
    Works for positive and negative scalars.
    """

    if k == 0 or P is None:
        return None

    # Handle negative scalar
    if k < 0:
        return scalar_mul(-k, point_neg(P, p), a, p)

    result = None  # point at infinity
    addend = P

    while k:
        if k & 1:
            result = point_add(result, addend, a, p)

        addend = point_double(addend, a, p)
        k >>= 1

    return result


def point_add(P, Q, a, p):
    """
    Add two points P and Q on elliptic curve over F_p.
    Curve: y^2 = x^3 + ax + b
    """
    # Handle point at infinity
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # P + (-P) = O
    if x1 == x2 and (y1 %p != y2 % p):
        return None

    # If points are equal -> doubling
    if P == Q:
        if y1==0:
            return None;
        else:
            return point_double(P, a, p)

    # Regular addition
    slope = ((y2 - y1)  mod_inv(x2 - x1, p)) % p
    x3 = (slope  slope - x1 - x2) % p
    y3 = (slope  (x1 - x3) - y1) % p
    return (x3, y3)

def point_double(P, a, p):
    """
    Double a point P on elliptic curve over F_p.
    """
    if P is None:
        return None
    x, y = P
    # Tangent is vertical
    if y == 0:
        return None
    slope = ((3  x  x + a)  mod_inv(2  y, p)) % p
    x3 = (slope  slope - 2  x) % p
    y3 = (slope * (x - x3) - y) % p
    return (x3, y3)
