import streamlit as st

def mod_inv(n, p):
    return pow(n, p - 2, p)

def is_on_curve(P, a, b, p):
    if P is None: return True
    x, y = P
    return (y**2 - (x**3 + a*x + b)) % p == 0

def ecc_fp():
    # استفاده از دو ستون اصلی برای پر کردن عرض صفحه
    main_col, side_col = st.columns([2, 1])

    with main_col:
        st.subheader("🔢 Curve Calculation")
        
        # ردیف اول: پارامترها
        c1, c2, c3 = st.columns(3)
        with c1: p = st.number_input("Prime Field (p)", value=17, step=1)
        with c2: a = st.number_input("Parameter (a)", value=2, step=1)
        with c3: b = st.number_input("Parameter (b)", value=2, step=1)

        st.divider()

        # بخش عملیات با چیدمان افقی
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
            
            # منطق محاسبه P+Q در اینجا قرار می‌گیرد...
            
        else:
            with inner_col1:
                st.write("**Point P**")
                x1 = st.number_input("x1", value=5)
                y1 = st.number_input("y1", value=1)
            with inner_col2:
                st.write("**Scalar Value**")
                k = st.number_input("k (integer)", value=2)

    with side_col:
        st.subheader("📖 Math Reference")
        st.info("Elliptic Curves over finite fields are crucial for ZK-SNARKs.")
        
        # نمایش فرمول زنده بر اساس مقادیر ورودی
        st.latex(f"E: y^2 \\equiv x^3 + {a if a else 'a'}x + {b if b else 'b'} \\pmod{{{p if p else 'p'}}}")
        
        with st.expander("Show Addition Law", expanded=True):
            st.latex(r"s = \frac{y_2 - y_1}{x_2 - x_1} \pmod{p}")
            st.latex(r"x_3 = s^2 - x_1 - x_2 \pmod{p}")
            st.latex(r"y_3 = s(x_1 - x_3) - y_1 \pmod{p}")

        # نمایش لیست نقاط (برای پارامترهای کوچک)
        if p and p < 50:
            points = []
            for x in range(p):
                for y in range(p):
                    if (y**2 - (x**3 + a*x + b)) % p == 0:
                        points.append(f"({x},{y})")
            st.write(f"**All points on this curve ({len(points)}):**")
            st.caption(", ".join(points[:20]) + ("..." if len(points) > 20 else ""))
