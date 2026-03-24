import streamlit as st
import matplotlib.pyplot as plt

def ecc_fp():
    points_list = []
    x_coords = []
    y_coords = []
    
    col1, col2 = st.columns([8, 5])

    with col1:
        with st.expander("Curve Definition", expanded=True):
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
            
            with st.expander(f"📍 Points on curve ({len(points_list)+1} points):", expanded=True):
                points_html = f"""
                    <div style='font-family: monospace; font-size: 16px; line-height: 1.6; color: #2c3e50; padding: 5px 0px; word-break: break-all;'>
                        {{ {all_points_str} }}
                    </div>
                """
                st.markdown(points_html, unsafe_allow_html=True)

        with st.expander("Point Addition Formulas", expanded=True):
            st.latex(r"s = \frac{y_Q - y_P}{x_Q - x_P} \pmod{p}")
            st.latex(r"x_R = s^2 - x_P - x_Q \pmod{p}")
            st.latex(r"y_R = s(x_P - x_R) - y_P \pmod{p}")

        st.divider()

        op = st.radio("Choose Operation:", ["Point Addition (P + Q)", "Scalar Multiplication (nP)"], horizontal=True)
        
        if op == "Point Addition (P + Q)":
            st.write("**Enter Coordinates for P and Q:**")
            cols = st.columns([0.4, 1, 0.2, 1, 0.4, 0.6, 0.4, 1, 0.2, 1, 0.4, 0.6, 0.4, 1, 0.2, 1, 0.4])
            symbol_style = "<div style='text-align: center; font-size: 24px; font-weight: bold; line-height: 45px; height: 45px;'>"
        
            with cols[0]: st.markdown(f"{symbol_style}(</div>", unsafe_allow_html=True)
            with cols[1]: xP = st.number_input("xP", value=None, key="xP", label_visibility="collapsed")
            with cols[2]: st.markdown(f"{symbol_style},</div>", unsafe_allow_html=True)
            with cols[3]: yP = st.number_input("yP", value=None, key="yP", label_visibility="collapsed")
            with cols[4]: st.markdown(f"{symbol_style})</div>", unsafe_allow_html=True)
            
            P = (xP, yP) if xP is not None and yP is not None else None
            
            with cols[5]: st.markdown(f"{symbol_style}+</div>", unsafe_allow_html=True)
            
            with cols[6]: st.markdown(f"{symbol_style}(</div>", unsafe_allow_html=True)
            with cols[7]: xQ = st.number_input("xQ", value=None, key="xQ", label_visibility="collapsed")
            with cols[8]: st.markdown(f"{symbol_style},</div>", unsafe_allow_html=True)
            with cols[9]: yQ = st.number_input("yQ", value=None, key="yQ", label_visibility="collapsed")
            with cols[10]: st.markdown(f"{symbol_style})</div>", unsafe_allow_html=True)
            
            Q = (xQ, yQ) if xQ is not None and yQ is not None else None

            if P and not is_on_curve(P, a, b, p):
                st.error("The point P is not on the curve.")
            if Q and not is_on_curve(Q, a, b, p):
                st.error("The point Q is not on the curve.")

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
