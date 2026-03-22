import streamlit as st
from modules.styles import apply_styles
from views.header_view import render_header_view
from views.cryptography_view import render_cryptography_tab
from views.blockchain_view import render_blockchain_tab
from views.zkp_view import render_zkp_tab

# تنظیمات اولیه صفحه
st.set_page_config(
    page_title="Clear Cypher Lab", 
    page_icon="logo.png", 
    layout="wide"
)

# حذف تهاجمی هدر و پدینگ‌های اضافه
st.markdown("""
    <style>
        /* حذف نوار بالایی استریم‌لیت */
        header[data-testid="stHeader"] {
            display: none !important;
        }

        /* حذف پدینگ بدنه اصلی و کشیدن محتوا به سقف */
        .main .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            margin-top: -45px !important; /* جبران فضای خالی سیستم */
        }

        /* حذف فاصله خودکار بین ویجت‌ها برای فشرده‌سازی */
        [data-testid="stVerticalBlock"] > div {
            gap: 0.1rem !important;
        }

        /* مخفی کردن منوی تنظیمات و فوتر */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* تنظیم ارتفاع تب‌ها برای ظرافت بیشتر */
        button[data-baseweb="tab"] {
            height: 40px !important;
            padding-top: 0px !important;
            padding-bottom: 0px !important;
        }
    </style>
    """, unsafe_allow_html=True)

# اعمال استایل‌های اختصاصی پدینگ کناره‌ها
apply_styles()

# نمایش هدر سایت
render_header_view()

# ایجاد تب‌های اصلی ناوبری
tab1, tab2, tab3 = st.tabs(["🌐 Cryptography", "⛓️ Blockchain", "🔐 ZKP"])

with tab1: 
    render_cryptography_tab()
with tab2: 
    render_blockchain_tab()
with tab3: 
    render_zkp_tab()

st.divider()
