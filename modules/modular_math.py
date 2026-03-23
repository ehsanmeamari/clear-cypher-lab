import streamlit as st

def run_modular_math():
    st.subheader("Modular Arithmetic")
    
    # ایجاد دو ستون اصلی برای قرارگیری ماشین‌حساب‌ها کنار هم
    main_col1, main_col2 = st.columns(2)
    
    # --- ستون اول: Modulo Calculator ---
    with main_col1:
        with st.expander("🔢 Modulo Calculator", expanded=True):
            # زیرمجموعه ستون‌ها برای چیدمان داخلی (Input و Result)
            c1, c2, c3 = st.columns([1, 1, 1.2])
            with c1:
                num_a = st.number_input("a:", value=17, key="mod_calc_a")
            with c2:
                num_n = st.number_input("n:", value=5, key="mod_calc_n")
            with c3:
                st.markdown("<div style='margin-top: 28px;'>", unsafe_allow_html=True)
                if num_n != 0:
                    st.code(f"{num_a % num_n}", language="text")
                else:
                    st.error("Error")
                st.markdown("</div>", unsafe_allow_html=True)

    # --- ستون دوم: Modular Inverse ---
    with main_col2:
        with st.expander("🔄 Modular Inverse", expanded=True):
            # زیرمجموعه ستون‌ها برای چیدمان داخلی
            c1, c2, c3 = st.columns([1, 1, 1.2])
            with c1:
                inv_a = st.number_input("a:", value=3, key="inv_a")
            with c2:
                inv_n = st.number_input("n:", value=11, key="inv_n")
            with c3:
                st.markdown("<div style='margin-top: 28px;'>", unsafe_allow_html=True)
                try:
                    res_inv = pow(int(inv_a), -1, int(inv_n))
                    st.code(f"{res_inv}", language="text")
                except ValueError:
                    st.error("None")
                st.markdown("</div>", unsafe_allow_html=True)
            
            # نمایش فرمول کوچک در پایین ستون دوم در صورت وجود معکوس
            try:
                res_inv = pow(int(inv_a), -1, int(inv_n))
                st.latex(f"{inv_a} \\cdot {res_inv} \\equiv 1 \\pmod{{{inv_n}}}")
            except:
                pass
