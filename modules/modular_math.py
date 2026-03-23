import streamlit as st

def run_modular_math():
    st.subheader("Modular Arithmetic")
    
    # Horizontal sub-menu for Modular Arithmetic
    mod_sub_module = st.radio(
        label="Sub Operation:",
        options=["Modulo Calculator", "Modular Inverse"],
        key="mod_sub_selection",
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.divider()
    
    if mod_sub_module == "Modulo Calculator":
        with st.expander("🔢 Modulo Calculator", expanded=True):
            # ایجاد ۳ ستون: دو ستون برای ورودی و یکی برای نتیجه
            col1, col2, col3 = st.columns([1, 1, 1.5])
            
            with col1:
                num_a = st.number_input("Enter number (a):", value=17, key="mod_calc_a")
            with col2:
                num_n = st.number_input("Enter modulo (n):", value=5, key="mod_calc_n")
            
            with col3:
                if num_n != 0:
                    result = num_a % num_n
                    # اضافه کردن فاصله برای تراز شدن با اینپوت‌ها
                    st.markdown("<div style='margin-top: 28px;'>", unsafe_allow_html=True)
                    st.code(f"{num_a} mod {num_n} = {result}", language="text")
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='margin-top: 28px;'>", unsafe_allow_html=True)
                    st.error("Error: Div by 0")
                    st.markdown("</div>", unsafe_allow_html=True)

    elif mod_sub_module == "Modular Inverse":
        # Same here: all code under ELIF must be indented
        with st.expander("🔄 Modular Multiplicative Inverse", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                inv_a = st.number_input("Enter number (a):", value=3, key="inv_a")
            with col2:
                inv_n = st.number_input("Enter modulo (n):", value=11, key="inv_n")
            
            try:
                # pow(a, -1, n) calculates modular inverse
                res_inv = pow(int(inv_a), -1, int(inv_n))
                st.success(f"Result: {res_inv}")
                st.latex(f"{inv_a} \\cdot {res_inv} \\equiv 1 \\pmod{{{inv_n}}}")
            except ValueError:
                st.error(f"Modular inverse does not exist for {inv_a} mod {inv_n}.")
                st.info("Note: Inverse exists only if gcd(a, n) = 1.")
