import streamlit as st
import matplotlib.pyplot as plt

def ecc_fp():
    points_list = []
    x_coords = []
    y_coords = []
    
    # Split the page into two equal columns as per the image
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
