import streamlit as st
import re

st.set_page_config(page_title="Clear Cypher Lab", page_icon="🛡️")

# Styling for a professional look
st.title("🛡️ Clear Cypher Lab")
st.subheader("Welcome to the ClearCypherLab")

st.markdown("""
This lab is designed for interactive learning of complex security concepts, 
Blockchain, and Cyber Security.
""")

st.divider()

# Tool: Password Strength Checker
st.header("🕵️ Password Strength Analyzer")
password = st.text_input("Enter a password to test (Local test, not stored):", type="password")

if password:
    # Calculating score
    score = 0
    if len(password) >= 8: score += 1
    if re.search("[a-z]", password) and re.search("[A-Z]", password): score += 1
    if re.search("[0-9]", password): score += 1
    if re.search("[!@#$%^&*]", password): score += 1

    # Displaying Results
    results = [
        {"label": "Very Weak ❌", "color": "error"},
        {"label": "Weak ⚠️", "color": "warning"},
        {"label": "Medium ✅", "color": "info"},
        {"label": "Strong 🟢", "color": "success"},
        {"label": "Excellent 💪", "color": "success"}
    ]
    
    res = results[score]
    if score <= 1: st.error(f"Status: {res['label']}")
    elif score == 2: st.warning(f"Status: {res['label']}")
    else: st.success(f"Status: {res['label']}")

st.divider()
st.info("Stay tuned for upcoming modules: AES Encryption, RSA Visualizer, and Blockchain Explorer.")
