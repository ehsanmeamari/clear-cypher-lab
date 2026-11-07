import streamlit as st
from modules.computer.binary import render_binary_tab

def render_computer_tab():
    computer_module = st.radio(
        "Select Module",
        options=["Binary", "OSI Model", "Computer Networks"],
        horizontal=True,
        label_visibility="collapsed",
        key="computer_module"
    )

    st.divider()
    
    if computer_module == "Binary":
        render_binary_tab()
    elif computer_module == "OSI Model":
        st.info("OSI Model Simulator will be implemented here.")
    elif computer_module == "Computer Networks":
        st.info("Computer Networks Lab will be implemented here.")
