import streamlit as st
import re

st.set_page_config(page_title="Clear Cypher Lab", page_icon="🛡️")
st.title("🛡️ Clear Cypher Lab")
st.subheader("به آزمایشگاه شفاف رمزنگاری خوش آمدید")

st.divider()
st.header("🕵️ ابزار تست قدرت گذرواژه")
password = st.text_input("یک پسورد وارد کنید:", type="password")

if password:
    score = sum([len(password) >= 8, 
                 bool(re.search("[a-z]", password) and re.search("[A-Z]", password)),
                 bool(re.search("[0-9]", password)),
                 bool(re.search("[!@#$%^&*]", password))])
    
    results = ["بسیار ضعیف ❌", "ضعیف ⚠️", "متوسط ✅", "خوب 🟢", "عالی و امن 💪"]
    st.write(f"وضعیت: {results[score]}")

st.divider()
st.info("این آزمایشگاه محلی برای یادگیری تعاملی امنیت است.")
