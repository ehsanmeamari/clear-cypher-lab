import streamlit as st

def render_binary_tab():
    st.subheader("Binary Simulators & Converters")
    
    mode = st.radio(
        "Select Converter Type",
        options=["Decimal to Binary (16-bit)", "Text to Binary (ASCII)"],
        horizontal=True,
        key="binary_mode"
    )
    
    st.divider()
    
    if mode == "Decimal to Binary (16-bit)":
        st.markdown("### Decimal to Binary Converter (16-bit)")
        
        decimal_val = st.number_input(
            "Enter a Decimal Number (0 to 65535):", 
            min_value=0, 
            max_value=65535, 
            value=5, 
            step=1
        )
        
        binary_val = format(decimal_val, '016b')
        formatted_binary = " ".join([binary_val[i:i+4] for i in range(0, 16, 4)])
        
        st.markdown("16-bit Binary Representation:")
        st.code(formatted_binary, language="text")
        
        st.write("Bit Visualization:")
        cols = st.columns(16)
        for i, bit in enumerate(binary_val):
            with cols[i]:
                st.metric(label=f"Bit {15-i}", value=bit)
                
    else:
        st.markdown("### Text to Binary Converter (ASCII)")
        
        text_val = st.text_input("Enter Text:", value="You good?")
        
        if text_val:
            binary_chars = [format(ord(char), '08b') for char in text_val]
            full_binary = " ".join(binary_chars)
            
            st.markdown("ASCII Binary Representation:")
            st.code(full_binary, language="text")
            
            st.write("Character Breakdown:")
            for char, b_code in zip(text_val, binary_chars):
                cols = st.columns(2)
                with cols[0]:
                    st.code(f"'{char}' (ASCII: {ord(char)})")
                with cols[1]:
                    st.code(b_code)
