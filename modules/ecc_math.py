import streamlit as st
import matplotlib.pyplot as plt

def ecc_fp():
    points_list = []
    x_coords = []
    y_coords = []
    
    # Divide the page into two equal columns as per the image
    left_col, right_col = st.columns([1, 1]) 

    with left_col: 
        # Create an expander with a specific title
        with st.expander("Curve Definition", expanded=True): 
            # Now only 4 columns are needed (three for numbers, one for the formula)
            c1, c2, c3, c4 = st.columns([1, 1, 1, 2.5]) 
                                    
            with c1:  
                p = st.number_input("Prime Field (p)", value=17, step=1) 
            with c2:  
                a = st.number_input("Parameter (a)", value=2, step=1) 
            with c3:  
                b = st.number_input("Parameter (b)", value=13, step=1) 
                                     
            with c4: 
                # Vertical alignment of the formula (25px is usually enough inside an expander)
                st.markdown("<div style='margin-top: 25px;'>", unsafe_allow_html=True) 
                st.latex(f"E: y^2 \\equiv x^3 + {a}x + {b} \\pmod{{{p}}}") 
                st.markdown("</div>", unsafe_allow_html=True) 
        
        # Place the divider after the expander block ends
        st.divider() 

        # 1. Curve point calculations 
        if p and p < 1000: 
            for x in range(p): 
                for y in range(p): 
                    if (y**2 - (x**3 + a*x + b)) % p == 0: 
                        points_list.append((x, y)) 
                        x_coords.append(x) 
                        y_coords.append(y) 

        # 2. Display the list of points (before the plot) enclosed in brackets and compact 
        if points_list: 
            str_points = [f"({pt[0]},{pt[1]})" for pt in points_list] 
            
            if len(str_points) > 30: 
                core_points = ", ".join(str_points[:30]) + ", ..." 
            else: 
                core_points = ", ".join(str_points) 
            
            # Remove space at the beginning of brackets for more compactness 
            points_in_brackets = f"{{{core_points}}}" 
            
            # Change font to Sans-Serif and reduce letter spacing to fit in fewer lines 
            combined_html = f""" 
                <div style='font-size: 18px; line-height: 1.4; margin-bottom: 20px;'> 
                    <span style='font-weight: bold; color: #31333F;'>Points on curve ({len(points_list)} points):</span> 
                    <span style='color: #555; margin-left: 5px; font-family: sans-serif; letter-spacing: -0.5px;'>{points_in_brackets}</span> 
                </div> 
            """ 
            st.markdown(combined_html, unsafe_allow_html=True) 
            
        # 3. Visual plot rendering 
        st.write(f"**Visualization over Fp (p={p}):**") 
        fig, ax = plt.subplots(figsize=(6, 6)) 
        
        # s value changed from 50 to 20 (for smaller circles) 
        # linewidth changed from 1.5 to 1.0 (for more elegance in small size) 
        ax.scatter(x_coords, y_coords, s=20, facecolors='none', edgecolors='#3498db', linewidth=1.0) 
        
        ax.set_xlim(-0.5, p - 0.5) 
        ax.set_ylim(-0.5, p - 0.5) 
        ax.grid(True, linestyle='-', alpha=0.3) 
        ax.set_xlabel("x") 
        ax.set_ylabel("y") 
        ax.set_xticks(range(0, p, max(1, p // 10))) 
        ax.set_yticks(range(0, p, max(1, p // 10))) 
        st.pyplot(fig) 

    with right_col:                 
        with st.expander("Point Addition Formulas", expanded=True): 
            st.latex(r"s = \frac{y_Q - y_P}{x_Q - x_P} \pmod{p}") 
            st.latex(r"x_R = s^2 - x_P - x_Q \pmod{p}") 
            st.latex(r"y_R = s(x_P - x_R) - y_P \pmod{p}") 

        st.divider() 

        # Math operations section in a linear layout 
        op = st.radio("Choose Operation:", ["Point Addition (P + Q)", "Scalar Multiplication (nP)"], horizontal=True) 
        
        if op == "Point Addition (P + Q)": 
            st.write("**Enter Coordinates for P and Q:**") 
            # 17 columns to align brackets and fields in one line 
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
            with
