# در فایل app.py، بخشی که با with st.sidebar شروع می‌شود را پیدا کن و به این شکل تغییر بده:

with st.sidebar:
    st.title("🛡️ Navigation")
    st.markdown("---") # خط جداکننده
    
    st.write("🔗 **Social Media:**")
    
    # ایجاد دو ستون برای قرارگیری آیکون‌ها کنار هم
    col_yt, col_li = st.columns(2)
    
    with col_yt:
        # دکمه یوتیوب
        st.markdown(
            """
            <a href="https://www.youtube.com/@ClearCypherLab" target="_blank">
                <img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" width="100%">
            </a>
            """, 
            unsafe_allow_html=True
        )
        
    with col_li:
        # دکمه لینکدین (لینک عددی که فرستادی را اینجا گذاشتم)
        st.markdown(
            """
            <a href="https://www.linkedin.com/company/113012501/" target="_blank">
                <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" width="100%">
            </a>
            """, 
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # ادامه کدهای رادیو باتن برای انتخاب ماژول‌ها
    # ...
