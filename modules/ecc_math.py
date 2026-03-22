import streamlit as st

def ecc_fp():
    # تقسیم صفحه به دو ستون مساوی
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.subheader("🔢 Curve Definition")
        
        # ۱. دریافت ورودی‌های منحنی
        c1, c2, c3 = st.columns(3)
        with c1: p = st.number_input("Prime Field (p)", value=17, step=1)
        with c2: a = st.number_input("Parameter (a)", value=2, step=1)
        with c3: b = st.number_input("Parameter (b)", value=2, step=1)

        # نمایش فرمول منحنی
        st.latex(f"E: y^2 \\equiv x^3 + {a}x + {b} \\pmod{{{p}}}")
        st.divider()

        # نمایش لیست نقاط در ستون سمت چپ
        if p and p < 100:
            points = []
            for x in range(p):
                for y in range(p):
                    if (y**2 - (x**3 + a*x + b)) % p == 0:
                        points.append(f"({x},{y})")
            st.write(f"**Points on curve ({len(points)}):**")
            st.caption(", ".join(points[:30]) + ("..." if len(points) > 30 else ""))

    with right_col:        
        st.subheader("📖 Mathematical Context")
        with st.expander("Show Addition Law", expanded=True):
            st.latex(r"s = \frac{y_2 - y_1}{x_2 - x_1} \pmod{p}")
            st.latex(r"x_3 = s^2 - x_1 - x_2 \pmod{p}")
            st.latex(r"y_3 = s(x_1 - x_3) - y_1 \pmod{p}")

        st.divider()

        # ۲. انتقال بخش عملیات به ستون سمت راست (کادر قرمز مورد نظر شما)
        op = st.radio("Choose Operation:", ["Point Addition (P + Q)", "Scalar Multiplication (nP)"], horizontal=True)
        
        # قرار دادن ورودی‌های نقاط در زیر رادیو باتن (درون ستون سمت راست)
        if op == "Point Addition (P + Q)":
            st.write("**Enter Coordinates for P and Q:**")
            # ایجاد 4 ستون برای x1, y1, x2, y2 در یک خط
            ix1, iy1, ix2, iy2 = st.columns(4)
            with ix1: x1 = st.number_input("xP", value=5, key="x1")
            with iy1: y1 = st.number_input("yP", value=1, key="y1")
            with ix2: x2 = st.number_input("xR", value=6, key="x2")
            with iy2: y2 = st.number_input("yR", value=3, key="y2")
            
        else:
            st.write("**Enter Point P and Scalar n:**")
            # ایجاد 3 ستون برای x1, y1, n در یک خط
            ix1, iy1, in1 = st.columns(3)
            with ix1: x1 = st.number_input("xP", value=5, key="x1_k")
            with iy1: y1 = st.number_input("yP", value=1, key="y1_k")
            with in1: n = st.number_input("n", value=2, key="n_scalar")
