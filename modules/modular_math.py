import streamlit as st

def run_modular_math():
    st.subheader("Modular Arithmetic")
    
    # Using a clean layout with two main columns
    col_left, col_right = st.columns(2)
    
    with col_left:
        with st.expander("Modulo Calculator", expanded=True):
            # Layout: Input A, Input N, and the result in one row
            c1, c2, c3 = st.columns([1, 1, 1.2])
            with c1:
                val_a = st.number_input("a:", value=17, key="unique_mod_a")
            with c2:
                val_n = st.number_input("n:", value=5, key="unique_mod_n")
            with c3:
                st.markdown("<div style='margin-top:28px;'>", unsafe_allow_html=True)
                if val_n != 0:
                    st.code(f"{val_a % val_n}", language="text")
                else:
                    st.error("Error")
                st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        with st.expander("Modular Inverse", expanded=True):
            # Layout: Input A, Input N, and the result
            i1, i2, i3 = st.columns([1, 1, 1.2])
            with i1:
                inv_a = st.number_input("a:", value=3, key="unique_inv_a")
            with i2:
                inv_n = st.number_input("n:", value=11, key="unique_inv_n")
            with i3:
                st.markdown("<div style='margin-top:28px;'>", unsafe_allow_html=True)
                try:
                    res = pow(int(inv_a), -1, int(inv_n))
                    st.code(f"{res}", language="text")
                except:
                    st.error("None")
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Math formula
            try:
                res = pow(int(inv_a), -1, int(inv_n))
                st.latex(f"{inv_a} \\cdot {res} \\equiv 1 \\pmod{{{inv_n}}}")
            except:
                pass
