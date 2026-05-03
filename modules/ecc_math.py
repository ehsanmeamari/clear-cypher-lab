import streamlit as st
import matplotlib.pyplot as plt

def ecc_fp():
    points_list = []
    x_coords = []
    y_coords = []
    
    col1, col2 = st.columns([8, 5])

    with col1:
        with st.expander("Curve Definition", expanded=False):
            c1, c2, c3, c4 = st.columns([1, 1, 1, 2.5])            
            with c1: 
                p = st.number_input("Prime (p)", value=17, step=1)
            with c2: 
                a = st.number_input("Parameter (a)", value=2, step=1)
            with c3: 
                b = st.number_input("Parameter (b)", value=13, step=1)

            with c4:
                discriminant = 4*(a**3) + 27*(b**2)
                if discriminant == 0:
                    st.error("Singular Curve: Select another curve parameters")
                else:
                    st.markdown("<div style='margin-top: 25px;'>", unsafe_allow_html=True)
                    if a % p == 0:
                        st.latex(f"E: y^2 \\equiv x^3 + {b % p} \\pmod{{{p}}}")
                    elif b % p == 0:
                        st.latex(f"E: y^2 \\equiv x^3 + {a % p}x \\pmod{{{p}}}")
                    else:
                        st.latex(f"E: y^2 \\equiv x^3 + {a % p}x + {b % p} \\pmod{{{p}}}")
                    st.markdown("</div>", unsafe_allow_html=True)

        st.divider()

        if p and p < 1000 and discriminant != 0:
            for x in range(p):
                for y in range(p):
                    if (y**2 - (x**3 + a*x + b)) % p == 0:
                        points_list.append((x, y))
                        x_coords.append(x)
                        y_coords.append(y)

        if points_list:
            str_points = [f"({pt[0]},{pt[1]})" for pt in points_list]
            all_points_str = ", ".join(str_points)
            
            with st.expander(f"📍 Points on curve ({len(points_list)+1} points):", expanded=False):
                points_html = f"""
                    <div style='font-family: monospace; font-size: 16px; line-height: 1.6; color: #2c3e50; padding: 5px 0px; word-break: break-all;'>
                        {{ {all_points_str} }}
                    </div>
                """
                st.markdown(points_html, unsafe_allow_html=True)
                

        op = st.radio("Choose Operation:", ["Point Addition (P + Q)", "Scalar Multiplication (nP)"], horizontal=True)
        
        if op == "Point Addition (P + Q)":
            st.write("**Enter Coordinates for P and Q:**")
            cols = st.columns([0.4, 1, 0.2, 1, 0.4, 0.6, 0.4, 1, 0.2, 1, 0.4, 0.6, 0.4, 1, 0.2, 1, 0.4])
            symbol_style = "<div style='text-align: center; font-size: 24px; font-weight: bold; line-height: 45px; height: 45px;'>"
        
            with cols[0]: st.markdown(f"{symbol_style}(</div>", unsafe_allow_html=True)
            with cols[1]: xP = st.number_input("xP", value=None, key="xP", label_visibility="collapsed", step=1, format="%d")
            with cols[2]: st.markdown(f"{symbol_style},</div>", unsafe_allow_html=True)
            with cols[3]: yP = st.number_input("yP", value=None, key="yP", label_visibility="collapsed", step=1, format="%d")
            with cols[4]: st.markdown(f"{symbol_style})</div>", unsafe_allow_html=True)
            
            P = (xP, yP) if xP is not None and yP is not None else None
            
            with cols[5]: st.markdown(f"{symbol_style}+</div>", unsafe_allow_html=True)
            
            with cols[6]: st.markdown(f"{symbol_style}(</div>", unsafe_allow_html=True)
            with cols[7]: xQ = st.number_input("xQ", value=None, key="xQ", label_visibility="collapsed", step=1, format="%d")
            with cols[8]: st.markdown(f"{symbol_style},</div>", unsafe_allow_html=True)
            with cols[9]: yQ = st.number_input("yQ", value=None, key="yQ", label_visibility="collapsed", step=1, format="%d")
            with cols[10]: st.markdown(f"{symbol_style})</div>", unsafe_allow_html=True)
            
            Q = (xQ, yQ) if xQ is not None and yQ is not None else None

            if P and not is_on_curve(P, a, b, p):
                st.error("The first point is not on the curve.")
            if Q and not is_on_curve(Q, a, b, p):
                st.error("The second point is not on the curve.")

            if P is None or Q is None:
                st.warning("Input both points")
            else:
                if is_on_curve(P, a, b, p) and is_on_curve(Q, a, b, p):
                    R = point_add(P, Q, a, p)
                    with cols[11]: st.markdown(f"{symbol_style}=</div>", unsafe_allow_html=True)
                    with cols[12]: st.markdown(f"{symbol_style}(</div>", unsafe_allow_html=True)
                    with cols[13]: st.number_input("xR", value=R[0], key="xR", label_visibility="collapsed")
                    with cols[14]: st.markdown(f"{symbol_style},</div>", unsafe_allow_html=True)
                    with cols[15]: st.number_input("yR", value=R[1], key="yR", label_visibility="collapsed")
                    with cols[16]: st.markdown(f"{symbol_style})</div>", unsafe_allow_html=True)
        if op == "Scalar Multiplication (nP)":
            st.write("**Enter Scalar n and Point P:**")
            
            cols = st.columns([1, 0.4, 0.4, 1, 0.2, 1, 0.2, 0.3, 0.2, 1.2, 0.2, 1.2, 0.2])
            
            symbol_style = "<div style='text-align: center; font-size: 24px; font-weight: bold; line-height: 45px; height: 45px;'>"

            # Scalar n
            with cols[0]:
                n = st.number_input("Scalar n", value=None, key="n_scalar", 
                                    label_visibility="collapsed", step=1, format="%d", min_value=0)

            # Multiplication symbol
            with cols[1]:
                st.markdown(f"{symbol_style}×</div>", unsafe_allow_html=True)

            # Point P
            with cols[2]:
                st.markdown(f"{symbol_style}(</div>", unsafe_allow_html=True)
            with cols[3]:
                xP = st.number_input("xP", value=None, key="xP_scalar", 
                                    label_visibility="collapsed", step=1, format="%d")
            with cols[4]:
                st.markdown(f"{symbol_style},</div>", unsafe_allow_html=True)
            with cols[5]:
                yP = st.number_input("yP", value=None, key="yP_scalar", 
                                    label_visibility="collapsed", step=1, format="%d")
            with cols[6]:
                st.markdown(f"{symbol_style})</div>", unsafe_allow_html=True)

            P = (xP % p, yP % p ) if xP is not None and yP is not None else None

            if P and not is_on_curve(P, a, b, p):
                st.error("The point is not on the curve.")

            if n is None or P is None:
                st.warning("Please enter both the scalar n and the point P.")
            else:
                if is_on_curve(P, a, b, p):
                    R = scalar_mul(n, P, a, p)   # your scalar multiplication function

                    with cols[7]:
                        st.markdown(f"{symbol_style}=</div>", unsafe_allow_html=True)

                    if R is None:
                        # ==================== POINT AT INFINITY CASE ====================
                        with cols[8]: st.markdown(f"{symbol_style}(</div>", unsafe_allow_html=True)
                        
                        with cols[9]:
                            st.markdown("""
                                <div style="text-align: center; font-size: 28px; font-weight: bold; 
                                            line-height: 52px; height: 52px;">
                                    ∞
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with cols[10]: st.markdown(f"{symbol_style},</div>", unsafe_allow_html=True)
                        
                        with cols[11]:st.markdown("""
                                <div style="text-align: center; font-size: 28px; font-weight: bold; 
                                            line-height: 52px; height: 52px;">
                                    ∞
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with cols[12]: st.markdown(f"{symbol_style})</div>", unsafe_allow_html=True)

                        st.caption("**Result:** Point at infinity 𝒪")

                    else:
                        # ==================== NORMAL POINT CASE ====================
                        with cols[8]: st.markdown(f"{symbol_style}(</div>", unsafe_allow_html=True)
                        with cols[9]: st.number_input("xR", value=R[0], key="xR", label_visibility="collapsed", disabled=True,step=None)
                        with cols[10]: st.markdown(f"{symbol_style},</div>", unsafe_allow_html=True)
                        with cols[11]: st.number_input("yR", value=R[1], key="yR", label_visibility="collapsed", disabled=True,step=None)
                        with cols[12]: st.markdown(f"{symbol_style})</div>", unsafe_allow_html=True)
                        
                        


def mod_inv(n, p):
    return pow(n, p - 2, p)


def is_on_curve(P, a, b, p):
    """Check whether a point lies on the curve."""
    if P is None:
        return True

    x, y = P
    return (y * y - (x * x * x + a * x + b)) % p == 0
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
    Compute k * P using double-and-add.
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


def point_add(P, Q, a, p ):
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
    if x1 % p == x2 % p  and (y1 % p != y2 % p):
        return None

    # If points are equal -> doubling
    if P == Q:
        if y1 % p ==0:
            return None;
        else:
            return point_double(P, a, p)

    # Regular addition
    slope = ((y2 - y1) * mod_inv(x2-x1, p)) % p #mod_inv(x2 - x1, p)) % p

    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p

    return (x3, y3)

 
def point_double(P, a, p):
    """
    Double a point P on elliptic curve over F_p.
    """
    if P is None:
        return None

    x, y = P

    # Tangent is vertical
    if y  % p == 0:
        return None

    slope = ((3 * x * x + a) * mod_inv(2 * y, p)) %p 

    x3 = (slope * slope - 2 * x) % p
    y3 = (slope * (x - x3) - y) % p

    return (x3, y3)

