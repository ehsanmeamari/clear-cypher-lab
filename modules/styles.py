import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem; 
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)
