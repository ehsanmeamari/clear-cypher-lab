import streamlit as st
import matplotlib.pyplot as plt

def ecc_fp():
    points_list = []
    x_coords = []
    y_coords = []
    
    # Divide the page into four equal columns
    col1, col2, col3, col4 = st.columns([6, 1, 2, 5])

    with col1:
        # 1. Create expander with clear title
        with st.expander("Curve Definition", expanded=True): # Already True
            # 4 columns: three for inputs, one for the formula
            c1, c2, c3, c4 = st.columns([1, 1, 1, 2.5])            
            with c1: 
                p = st.number_input("Prime (p)", value=17, step=1)
            with c2: 
                a = st.number_input("Parameter (a)", value=2, step=1)
            with c3: 
                b = st.number_input("Parameter (b)", value=13, step=1)

            with c4:
                # Vertical alignment for the formula
                st.markdown("<div style='margin-top: 25px;'>", unsafe_allow_html=True)
                st.latex(f"E: y^2 \\equiv x^3 + {a}x + {b} \\pmod{{{p}}}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Divider after the expander
        st.divider()

        # 2. Calculate points on the curve and then Display them
        if p and p < 1000:
            for x in range(p):
                for y in range(p):
                    if (y**2 - (x**3 + a*x + b)) % p == 0:
                        points_list.append((x, y))
                        x_coords.append(x)
                        y_coords.append(y)

        # 3. Display the list of points in an expander
        if points_list:
            str_points = [f"({pt[0]},{pt[1]})" for pt in points_list]
            all_points_str = ", ".join(str_points)
            
            # Using st.expander with expanded=True to keep it open by default
            with st.expander(f"📍 Points on curve ({len(points_list)} points):", expanded=True):
                # Removed the gray background div and used direct styled text
                points_html = f"""
                    <div style='
                        font-family: monospace; 
                        font-size: 16px; 
                        line-height: 1.6;
                        color: #2c3e50;
                        padding: 5px 0px;
                        word-break: break-all;'>
                        {{ {all_points_str} }}
                    </div>
                """
                st.markdown(points_html, unsafe_allow_html=True)

        # 4. Display Point Addition Formulas
        with st.expander("Point Addition Formulas", expanded=True):
            st.latex(r"s = \frac{y_Q - y_P}{x_Q - x_P} \pmod{p}")
            st.latex(r"x_R = s^2 - x_P - x_Q \pmod{p}")
            st.latex(r"y_R = s(x_P - x_R) - y_P \pmod{p}")

        st.divider()

        # 5. Mathematical operations section
        op = st.radio("Choose Operation:", ["Point Addition (P + Q)", "Scalar Multiplication (nP)"], horizontal=True)
        
        if op == "Point Addition (P + Q)":
            st.write("**Enter Coordinates for P and Q:**")
            # 17 columns for aligning parentheses and fields in one line
            cols = st.columns([0.4, 1, 0.2, 1, 0.4, 0.6, 0.4, 1, 0.2, 1, 0.4, 0.6, 0.4, 1, 0.2, 1, 0.4])

            symbol_style = "<div style='text-align: center; font-size: 24px; font-weight: bold; line-height: 45px; height: 45px;'>"
        
            # Display point pairs as (x, y)
            with cols[0]: st.markdown(f"{symbol_style}(</div>", unsafe_allow_html=True)
            with cols[1]: xP = st.number_input("xP", value=5, key="xP", label_visibility="collapsed")
            with cols[2]: st.markdown(f"{symbol_style},</div>", unsafe_allow_html=True)
            with cols[3]: yP = st.number_input("yP", value=1, key="yP", label_visibility="collapsed")
            with cols[4]: st.markdown(f"{symbol_style})</div>", unsafe_allow_html=True)
            
            with cols[5]: st.markdown(f"{symbol_style}+</div>", unsafe_allow_html=True)
            
            with cols[6]: st.markdown(f"{symbol_style}(</div>", unsafe_allow_html=True)
            with cols[7]: xQ = st.number_input("xQ", value=6, key="xQ", label_visibility="collapsed")
            with cols[8]: st.markdown(f"{symbol_style},</div>", unsafe_allow_html=True)
            with cols[9]: yQ = st.number_input("yQ", value=3, key="yQ", label_visibility="collapsed")
            with cols[10]: st.markdown(f"{symbol_style})</div>", unsafe_allow_html=True)
            
            with cols[11]: st.markdown(f"{symbol_style}=</div>", unsafe_allow_html=True)
            
            with cols[12]: st.markdown(f"{symbol_style}(</div>", unsafe_allow_html=True)
            with cols[13]: xR = st.number_input("xR", value=0, key="xR", label_visibility="collapsed")
            with cols[14]: st.markdown(f"{symbol_style},</div>", unsafe_allow_html=True)
            with cols[15]: yR = st.number_input("yR", value=0, key="yR", label_visibility="collapsed")
            with cols[16]: st.markdown(f"{symbol_style})</div>", unsafe_allow_html=True)           
            
        else:
            st.write("**Enter Point P and Scalar n:**")
            ix1, iy1, in1 = st.columns(3)
            with ix1: x1 = st.number_input("xP", value=5, key="x1_k")
            with iy1: y1 = st.number_input("yP", value=1, key="y1_k")
            with in1: n = st.number_input("n", value=2, key="n_scalar")    

    with col4:                 
        
        # Visual plot rendering inside an expander: Using expanded=True to keep the plot visible by default
        with st.expander(f"📊 Visualization over Fp (p={p}):", expanded=True):
            fig, ax = plt.subplots(figsize=(6, 6))
            
            # Scatter plot styling
            ax.scatter(x_coords, y_coords, s=20, facecolors='none', edgecolors='#3498db', linewidth=1.0)
            
            ax.set_xlim(-0.5, p - 0.5)
            ax.set_ylim(-0.5, p - 0.5)
            ax.grid(True, linestyle='-', alpha=0.3)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_xticks(range(0, p, max(1, p // 10)))
            ax.set_yticks(range(0, p, max(1, p // 10)))
            
            # Display the plot inside the expander
            st.pyplot(fig)
