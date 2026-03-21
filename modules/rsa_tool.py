import streamlit as st

def run_rsa_tool():
    st.subheader("🗝️ RSA Encryption Interactive Lab")
    st.info("RSA security relies on the difficulty of factoring the product of two large prime numbers.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 1. Pick Primes")
        p = st.number_input("Prime number p:", value=17)
        q = st.number_input("Prime number q:", value=11)
        
        n = p * q
        phi = (p-1) * (q-1)
        # Choosing a small public exponent e that is coprime with phi
        e = 7 
        
    with col2:
        st.markdown("### 2. Computed Values")
        st.code(f"Modulus (n) = p * q = {n}")
        st.code(f"Totient (φ) = (p-1)(q-1) = {phi}")
        st.code(f"Public Exponent (e) = {e}")

    st.divider()
    
    st.markdown("### 3. Test Encryption")
    message = st.number_input("Enter a number to encrypt (must be < n):", value=5)
    
    if message >= n:
        st.error(f"Message must be smaller than {n}")
    else:
        ciphertext = (message**e) % n
        st.success(f"Original Message: {message}")
        st.warning(f"Ciphertext (m^e mod n): {ciphertext}")
        st.caption("Formula: $C = m^e \pmod{n}$")
