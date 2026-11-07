import streamlit as st

def render_binary_tab():
    st.subheader("Binary Simulators & Converters")
    
    # انتخاب نوع تبدیل
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
        
        st.text_input("16-bit Binary Representation:", value=formatted_binary, disabled=True)
        
        st.write("Bit Visualization:")
        cols = st.columns(16)
        for i, bit in enumerate(binary_val):
            with cols[i]:
                st.metric(label=f"Bit {15-i}", value=bit)
                
    else:
        st.markdown("### Text to Binary Converter (ASCII)")
        
        text_val = st.text_input("Enter Text:", value="Hello")
        
        if text_val:
            # تبدیل هر کاراکتر به کد اسکی و سپس به باینری ۸ بیتی
            binary_chars = [format(ord(char), '08b') for char in text_val]
            full_binary = " ".join(binary_chars)
            
            st.text_input("ASCII Binary Representation:", value=full_binary, disabled=True)
            
            # نمایش جدول‌وار یا تفکیک‌شده برای هر کاراکتر
            st.write("Character Breakdown:")
            for char, b_code in zip(text_val, binary_chars):
                cols = st.columns(2)
                with cols[0]:
                    st.code(f"'{char}' (ASCII: {ord(char)})")
                with cols[1]:
                    st.code(b_code)
