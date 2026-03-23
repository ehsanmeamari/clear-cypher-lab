import streamlit as st

def run_modular_math():
    st.subheader("Modular Arithmetic")
    
    # Using two columns to separate the tools side-by-side
    m_col1, m_col2 = st.columns(2)
    
    with m_col1:
        with st.expander("🔢 Modulo Calculator", expanded=True):
            # Layout: Input A, Input N, and the result in one row
            ca, cn, cr = st.columns([1, 1, 1.2])
            with ca:
                v_a = st.number_input("a:", value=17, key="k_mod_a")
            with cn:
                v_n = st.number_input("n:", value=5, key="k_mod_n")
            with cr:
                st.markdown("<div style='margin-top:28px;'>", unsafe_allow_html=True)
                if v_n != 0:
                    st.code(f"{v_a % v_n}", language="text")
                else:
                    st.error("Error")
                st.markdown("</div>", unsafe_allow_html=True)

    with m_col2:
        with st.expander("🔄 Modular Inverse", expanded=True):
            # Layout: Input A, Input N, and the result
            ia, in_, ir = st.columns([1, 1, 1.2])
            with ia:
                v_ia = st.number_input("a:", value=3, key="k_inv_a")
            with in_:
                v_in = st.number_input("n:", value=11, key="k_inv_n")
            with ir:
                st.markdown("<div style='margin-top:28px;'>", unsafe_allow_html=True)
                try:
                    res = pow(int(v_ia), -1, int(v_in))
                    st.code(f"{res}", language="text")
                except:
                    st.error("None")
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Mathematical display
            try:
                res = pow(int(v_ia), -1, int(v_in))
                st.latex(f"{v_ia} \cdot {res} \equiv 1 \pmod{{{v_in}}}")
            except:
                pass
