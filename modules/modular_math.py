import streamlit as st

def run_modular_math():
    
    # 1. Modulo Calculator Section
    with st.expander("🔢 Modulo Calculator", expanded=True):
        col1, col2, col3 = st.columns([1, 1, 1.5])
        with col1:
            num_a = st.number_input("Enter number (a):", value=17, key="mod_calc_a")
        with col2:
            num_n = st.number_input("Enter modulo (n):", value=5, key="mod_calc_n")
        with col3:
            if num_n != 0:
                result = num_a % num_n
                st.markdown("<div style='margin-top: 28px;'>", unsafe_allow_html=True)
                st.code(f"{num_a} mod {num_n} = {result}", language="text")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='margin-top: 28px;'>", unsafe_allow_html=True)
                st.error("Div by zero!")
                st.markdown("</div>", unsafe_allow_html=True)

    # 2. Modular Inverse Section (Always visible now)
    with st.expander("🔄 Modular Multiplicative Inverse", expanded=True):
        col1, col2, col3 = st.columns([1, 1, 1.5])
        with col1:
            inv_a = st.number_input("Enter number (a):", value=3, key="inv_a")
        with col2:
            inv_n = st.number_input("Enter modulo (n):", value=11, key="inv_n")
        with col3:
            st.markdown("<div style='margin-top: 28px;'>", unsafe_allow_html=True)
            try:
                res_inv = pow(int(inv_a), -1, int(inv_n))
                st.code(f"Inverse: {res_inv}", language="text")
            except ValueError:
                st.error("No inverse exists")
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Displaying the LaTeX formula below for clarity if inverse exists
        try:
            res_inv = pow(int(inv_a), -1, int(inv_n))
            st.latex(f"{inv_a} \\cdot {res_inv} \\equiv 1 \\pmod{{{inv_n}}}")
        except:
            pass
