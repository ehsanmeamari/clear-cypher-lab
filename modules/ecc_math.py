import streamlit as st

def mod_inv(n, p):
    return pow(n, p - 2, p)

def is_on_curve(P, a, b, p):
    if P is None: return True
    x, y = P
    return (y**2 - (x**3 + a*x + b)) % p == 0

def ecc_fp():
    # تقسیم صفحه به دو ستون مساوی برای پر کردن عرض
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.subheader("🔢 Curve Definition")
        
        # بخش پارامترها
        c1, c2, c3 = st.columns(3)
        with c1: p = st.number_input("Prime Field (p)", value=17, step=1)
        with c2: a = st.number_input("Parameter (a)", value=2, step=1)
        with c3: b = st.number_input("Parameter (b)", value=2, step=1)

        # نمایش فرمول
        st.latex(f"E: y^2 \\equiv x^3 + {a}x + {b} \\pmod{{{p}}}")
        st.divider()

        # نمایش لیست نقاط در ستون سمت راست برای پر کردن فضا
        if p and p < 100:
            points = []
            for x in range(p):
                for y in range(p):
                    if (y**2 - (x**3 + a*x + b)) % p == 0:
                        points.append(f"({x},{y})")
            
            st.write(f"**Points on this curve ({len(points)}):**")
            # نمایش نقاط به صورت تگ‌های کوچک برای زیبایی
            st.caption(", ".join(points[:50]) + ("..." if len(points) > 50 else ""))

        
        # بخش انتخاب عملیات (بدون فاصله اضافه - رفع خطا)
        op = st.radio("Choose Operation:", ["Point Addition (P + Q)", "Scalar Multiplication (kP)"], horizontal=True)
        
        inner_col1, inner_col2 = st.columns(2)
        if op == "Point Addition (P + Q)":
            with inner_col1:
                st.write("**Point P**")
                x1 = st.number_input("x1", value=5, key="x1")
                y1 = st.number_input("y1", value=1, key="y1")
            with inner_col2:
                st.write("**Point Q**")
                x2 = st.number_input("x2", value=6, key="x2")
                y2 = st.number_input("y2", value=3, key="y2")
        else:
            with inner_col1:
                st.write("**Point P**")
                x1 = st.number_input("x1_k", value=5)
                y1 = st.number_input("y1_k", value=1)
            with inner_col2:
                st.write("**Scalar Value**")
                k = st.number_input("k (integer)", value=2)

    with right_col:
        st.subheader("📖 Mathematical Context")
        with st.expander("Show Addition Law", expanded=True):
            st.latex(r"s = \frac{y_2 - y_1}{x_2 - x_1} \pmod{p}")
            st.latex(r"x_3 = s^2 - x_1 - x_2 \pmod{p}")
            st.latex(r"y_3 = s(x_1 - x_3) - y_1 \pmod{p}")
        
        st.divider()
