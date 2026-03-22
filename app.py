if zkp_module == "Modular Arithmetic":
        st.subheader("Modular Arithmetic")
        
        # Horizontal radio buttons for sub-modules
        mod_sub_module = st.radio(
            label="Select Operation:",
            options=["Modulo Calculator", "Modular Inverse"],
            key="mod_sub_selection",
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.divider()
        
        if mod_sub_module == "Modulo Calculator":
            st.write("### 🔢 Modulo Calculator")
            col1, col2 = st.columns(2)
            with col1:
                num_a = st.number_input("Enter number (a):", value=17, key="mod_calc_a")
            with col2:
                num_n = st.number_input("Enter modulo (n):", value=5, key="mod_calc_n")
            
            if num_n != 0:
                result = num_a % num_n
                st.code(f"{num_a} mod {num_n} = {result}", language="text")
            else:
                st.error("Modulo by zero is not defined!")
            
        elif mod_sub_module == "Modular Inverse":
            st.write("### 🔄 Modular Multiplicative Inverse")
            st.write("Find $x$ such that: $a \\cdot x \\equiv 1 \\pmod{n}$")
            
            col1, col2 = st.columns(2)
            with col1:
                inv_a = st.number_input("Enter number (a):", value=3, key="inv_a")
            with col2:
                inv_n = st.number_input("Enter modulo (n):", value=11, key="inv_n")
            
            # Logic to find modular inverse
            try:
                # pow(a, -1, n) finds the modular inverse in Python 3.8+
                res_inv = pow(int(inv_a), -1, int(inv_n))
                st.success(f"The modular inverse is: {res_inv}")
                st.code(f"{inv_a} * {res_inv} ≡ 1 (mod {inv_n})", language="text")
            except ValueError:
                st.error(f"Modular inverse does not exist for {inv_a} mod {inv_n}.")
                st.info("Inverse exists only if gcd(a, n) = 1 (they are coprime).")
