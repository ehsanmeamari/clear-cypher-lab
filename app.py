import streamlit as st
from modules.styles import apply_styles
from views.header_view import render_header_view
from views.cryptography_view import render_cryptography_tab
from views.blockchain_view import render_blockchain_tab
from views.zkp_view import render_zkp_tab

st.set_page_config(
    page_title="Clear Cypher Lab", 
    page_icon="logo.png", 
    layout="wide"
)

# این بخش تمام فضاهای مخفی سیستم را حذف می‌کند
st.markdown("""
    <style>
        /* ۱. حذف نوار ابزار بالای صفحه (Header) */
        header[data-testid="stHeader"] {
            display: none !important;
        }

        /* ۲. حذف پدینگ بدنه اصلی و چسباندن محتوا به سقف */
        .main .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            margin-top: -30px !important; /* جبران فاصله باقی‌مانده */
        }

        /* ۳. حذف فضای خالی خودکار بین المان‌ها */
        [data-testid="stVerticalBlock"] > div {
            gap: 0rem !important;
        }

        /* ۴. مخفی کردن دکمه منو و موارد اضافه برای تمیزی */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* ۵. کاهش ارتفاع تب‌ها برای فشردگی بیشتر */
        button[data-baseweb="tab"] {
            height: 40px !important;
        }
    </style>
    """, unsafe_allow_html=True)

# اجرای استایل‌های جانبی
apply_styles()

# فراخوانی هدر
render_header_view()

# نوار تب‌ها
tab1, tab2, tab3 = st.tabs(["🌐 Cryptography", "⛓️ Blockchain", "🔐 ZKP"])

with tab1: render_cryptography_tab()
with tab2: render_blockchain_tab()
with tab3: render_zkp_tab()
