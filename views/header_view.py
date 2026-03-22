import streamlit as st

def render_header_view():
    # استفاده از استایل موضعی برای فشرده‌سازی هدر و حذف مارجین‌های پیش‌فرض
    st.markdown("""
        <style>
            /* حذف فاصله بالای اولین المان در هدر */
            .header-container {
                margin-top: -10px; 
                padding-top: 0px;
            }
            /* تنظیم فاصله جداکننده (Divider) زیر هدر */
            .header-divider {
                margin-top: 5px !important;
                margin-bottom: 10px !important;
                opacity: 0.3;
            }
        </style>
    """, unsafe_allow_html=True)

    # ایجاد محفظه اصلی هدر
    st.markdown('<div class="header-container">', unsafe_allow_html=True)

    # تقسیم‌بندی صفحه: چپ (خالی)، وسط (لوگو و متن)، راست (شبکه‌های اجتماعی)
    col_left, col_center, col_right = st.columns([1, 2.5, 1.2])

    with col_left:
        st.empty()

    with col_center:
        # نمایش لوگو و شعار تبلیغاتی با تراز وسط
        st.markdown(
            """
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <img src="https://raw.githubusercontent.com/ehsanmeamari/clear-cypher-lab/main/logo.png" width="150" style="margin-top: 5px;">
                <div style="font-size: 1.3em; color: #1a365d; margin-top: 10px; font-weight: 700; text-align: center; letter-spacing: 0.5px;">
                    Demystifying the Math of Cybersecurity
                </div>
                <div style="font-size: 0.92em; color: #4a5568; margin-top: 2px; font-weight: 400; text-align: center;">
                    Interactive Learning Environment for ZKP, ECC & Blockchain
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with col_right:
        # بخش شبکه‌های اجتماعی با چیدمان فشرده در سمت راست
        st.markdown("""
            <div style="display: flex; flex-direction: column; align-items: flex-end; width: 100%; padding-top: 10px;">
                <div style="font-weight: bold; font-size: 0.85em; color: #555; margin-bottom: 6px; white-space: nowrap;">
                    🔗 Social Media
                </div>
                <div style="display: flex; flex-direction: column; gap: 5px; align-items: flex-end;">
                    <a href="https://www.youtube.com/@ClearCypherLab" target="_blank" style="text-decoration: none;">
                        <div style="background-color: #FF0000; color: white; padding: 5px 12px; border-radius: 4px; font-weight: bold; font-size: 0.72em; width: 100px; text-align: center;">
                            📺 YOUTUBE
                        </div>
                    </a>
                    <a href="https://www.linkedin.com/company/113012501/" target="_blank" style="text-decoration: none;">
                        <div style="background-color: #0077B5; color: white; padding: 5px 12px; border-radius: 4px; font-weight: bold; font-size: 0.72em; width: 100px; text-align: center;">
                            🔗 LINKEDIN
                        </div>
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
    # استفاده از خط جداکننده فشرده به جای st.divider استاندارد
    st.markdown('<hr class="header-divider">', unsafe_allow_html=True)
