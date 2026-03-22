import streamlit as st
import matplotlib.pyplot as plt

def ecc_fp():
    points_list = []
    x_coords = []
    y_coords = []
    
    # تقسیم صفحه به دو ستون مساوی مطابق تصویر
    left_col, right_col = st.columns([1, 1])

    with left_col:
        # ایجاد ۵ ستون: ستون اول برای عنوان و بقیه برای پارامترها و فرمول
        # نسبت‌ها را طوری تنظیم می‌کنیم که فضای کافی برای هر بخش باشد
        # تنظیم نسبت ستون‌ها (کمی فضای ستون اول را برای ظرافت بیشتر کم کردیم)
        c_title, c1, c2, c3, c4 = st.columns([1, 0.8, 0.8, 0.8, 2.3])
                
        with c_title:
            # استفاده از font-size برای کنترل دقیق اندازه (مثلاً 20px) و تنظیم فاصله از بالا
            st.markdown("""
                <div style='margin-top: 32px; font-size: 20px; font-weight: bold;'>
                    🔢 Curve Definition
                </div>
                """, unsafe_allow_html=True)
                
        with c1: 
            p = st.number_input("Prime Field (p)", value=17, step=1)
        with c2: 
            a = st.number_input("Parameter (a)", value=2, step=1)
        with c3: 
            b = st.number_input("Parameter (b)", value=13, step=1)
                
        with c4:
            # تراز کردن عمودی فرمول لاتک
            st.markdown("<div style='margin-top: 35px;'>", unsafe_allow_html=True)
            st.latex(f"E: y^2 \\equiv x^3 + {a}x + {b} \\pmod{{{p}}}")
            st.markdown("</div>", unsafe_allow_html=True)
                        
        st.divider()

        # ۱. محاسبات نقاط منحنی
        if p and p < 1000:
            for x in range(p):
                for y in range(p):
                    if (y**2 - (x**3 + a*x + b)) % p == 0:
                        points_list.append((x, y))
                        x_coords.append(x)
                        y_coords.append(y)

        # ۲. نمایش لیست نقاط (قبل از نمودار) محصور در آکولاد و فشرده
        if points_list:
            str_points = [f"({pt[0]},{pt[1]})" for pt in points_list]
            
            if len(str_points) > 30:
                core_points = ", ".join(str_points[:30]) + ", ..."
            else:
                core_points = ", ".join(str_points)
            
            # حذف فضا در ابتدای آکولاد برای فشردگی بیشتر
            points_in_brackets = f"{{{core_points}}}"
            
            # تغییر فونت به Sans-Serif و کاهش فاصله حروف برای جایگیری در خطوط کمتر
            combined_html = f"""
                <div style='font-size: 18px; line-height: 1.4; margin-bottom: 20px;'>
                    <span style='font-weight: bold; color: #31333F;'>Points on curve ({len(points_list)} points):</span>
                    <span style='color: #555; margin-left: 5px; font-family: sans-serif; letter-spacing: -0.5px;'>{points_in_brackets}</span>
                </div>
            """
            st.markdown(combined_html, unsafe_allow_html=True)
            
        # ۳. رسم نمودار بصری
        st.write(f"**Visualization over Fp (p={p}):**")
        fig, ax = plt.subplots(figsize=(6, 6))
        
        # مقدار s از 50 به 20 تغییر یافت (برای دایره‌های کوچکتر)
        # مقدار linewidth از 1.5 به 1.0 تغییر یافت (برای ظرافت بیشتر در سایز کوچک)
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

        # بخش عملیات ریاضی به صورت خطی
        op = st.radio("Choose Operation:", ["Point Addition (P + Q)", "Scalar Multiplication (nP)"], horizontal=True)
        
        if op == "Point Addition (P + Q)":
            st.write("**Enter Coordinates for P and Q:**")
            # ۱۷ ستون برای تراز کردن پرانتزها و فیلدها در یک خط
            cols = st.columns([0.4, 1, 0.2, 1, 0.4, 0.6, 0.4, 1, 0.2, 1, 0.4, 0.6, 0.4, 1, 0.2, 1, 0.4])
            
            symbol_style = "<div style='text-align: center; font-size: 24px; font-weight: bold; line-height: 45px; height: 45px;'>"
        
            # نمایش جفت نقاط به صورت (x, y)
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
