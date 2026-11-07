import streamlit as st

def render_binary_tab():
    st.subheader("Decimal to Binary Converter (16-bit)")
    
    decimal_val = st.number_input(
        "Enter a Decimal Number (0 to 65535):", 
        min_value=0, 
        max_value=65535, 
        value=5, 
        step=1
    )
    
    binary_val = format(decimal_val, '016b')
    
    formatted_binary = " ".join([binary_val[i:i+4] for i in range(0, 16, 4)])
    
    st.text_input("16-bit Binary Representation:", value=formatted_binary, disabled=True)
    
    st.write("Bit Visualization:")
    cols = st.columns(16)
    for i, bit in enumerate(binary_val):
        with cols[i]:
            st.metric(label=f"Bit {15-i}", value=bit)
