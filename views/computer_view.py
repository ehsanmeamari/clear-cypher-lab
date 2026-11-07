import streamlit as st

def render_computer_tab():

    computer_module = st.radio(
        "Select Module",
        options=["OSI Model", "Computer Networks"],
        horizontal=True,
        label_visibility="collapsed",
        key="computer_module"
    )

    st.divider()
    if computer_module == "OSI Model":
        st.info("OSI Model Simulator will be implemented here.")
    elif computer_module == "Computer Networks":
        st.info("Computer Networks Lab will be implemented here.")
