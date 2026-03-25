with col_left:
        # --- Section 1: Curve Definition ---
        with st.expander("Curve Definition", expanded=True):
            input_row = st.columns([1, 1, 2])
            with input_row[0]:
                a = st.number_input("a", value=-1.0, step=0.1, format="%.1f", key="ecc_r_a")
            with input_row[1]:
                b = st.number_input("b", value=1.0, step=0.1, format="%.1f", key="ecc_r_b")
            
            discriminant = 4*(a**3) + 27*(b**2)
            
            with input_row[2]:
                if discriminant != 0:
                    st.markdown("<div style='padding-top: 25px;'>", unsafe_allow_html=True)
                    a_part = f"{a:+.1f}x" if a != 0 else ""
                    b_part = f"{b:+.1f}" if b != 0 else ""
                    st.latex(f"y^2 = x^3 {a_part} {b_part}")
                    st.markdown("</div>", unsafe_allow_html=True)

            st.divider()
            
            if discriminant == 0:
                st.error("Singular Curve: Δ = 0")
            else:
                st.info(f"Discriminant (Δ) = {discriminant:.2f}")

        # --- Section 2: Point Addition Formulas (New) ---
        with st.expander("Point Addition Formulas", expanded=True):
            st.markdown("**Slope (s):**")
            st.latex(r"s = \frac{y_Q - y_P}{x_Q - x_P}")
            
            st.markdown("**Resulting Point (R):**")
            st.latex(r"x_R = s^2 - x_P - x_Q")
            st.latex(r"y_R = s(x_P - x_R) - y_P")
            
            st.info("Note: For $P=Q$, use the doubling formula for $s$.")
