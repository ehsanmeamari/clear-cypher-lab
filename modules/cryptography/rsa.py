import streamlit as st
from math import gcd

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def find_e(phi):
    for x in range(2, phi):
        if gcd(x, phi) == 1:
            return x
    return None

def mod_inverse(e, phi):
    for d in range(2, phi):
        if (d * e) % phi == 1:
            return d
    return None

def run_rsa_tool():
    # --- Step 1: Pick Primes ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 1. Pick Primes")
        p = st.number_input("Prime number p:", value=17, min_value=2, step=1)
        q = st.number_input("Prime number q:", value=11, min_value=2, step=1)

    # Validate primes
    if not is_prime(int(p)):
        st.error(f"{int(p)} is not a prime number. Please enter a valid prime for p.")
        st.stop()

    if not is_prime(int(q)):
        st.error(f"{int(q)} is not a prime number. Please enter a valid prime for q.")
        st.stop()

    if p == q:
        st.error("p and q must be different prime numbers.")
        st.stop()

    p, q = int(p), int(q)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = find_e(phi)
    d = mod_inverse(e, phi)

    # --- Step 2: Computed Values ---
    with col2:
        st.markdown("### 2. Computed Values")
        st.code(f"Modulus     (n) = p × q = {p} × {q} = {n}")
        st.code(f"Totient    (φ) = (p-1)(q-1) = {p-1} × {q-1} = {phi}")
        st.code(f"Public Key  (e) = {e}   → gcd(e, φ) = 1 ✓")
        st.code(f"Private Key (d) = {d}   → (d × e) mod φ = 1 ✓")

    st.caption("📌 Public key: **(e, n)** — Private key: **(d, n)**")
    st.divider()

    # --- Step 3: Encrypt ---
    st.markdown("### 3. Encrypt a Message")
    message = st.number_input(f"Enter a number to encrypt (must be < {n}):", value=5, min_value=1, step=1)

    if message >= n:
        st.error(f"Message must be smaller than n = {n}")
        st.stop()

    message = int(message)
    ciphertext = pow(message, e, n)

    col3, col4 = st.columns(2)
    with col3:
        st.success(f"Original Message (m): **{message}**")
        st.caption(f"Formula: $C = m^e \\pmod{{n}}$")
        st.caption(f"$C = {message}^{{{e}}} \\pmod{{{n}}} = {ciphertext}$")
    with col4:
        st.warning(f"Ciphertext (C): **{ciphertext}**")

    st.divider()

    # --- Step 4: Decrypt ---
    st.markdown("### 4. Decrypt the Ciphertext")

    decrypted = pow(ciphertext, d, n)

    col5, col6 = st.columns(2)
    with col5:
        st.warning(f"Ciphertext (C): **{ciphertext}**")
        st.caption(f"Formula: $m = C^d \\pmod{{n}}$")
        st.caption(f"$m = {ciphertext}^{{{d}}} \\pmod{{{n}}} = {decrypted}$")
    with col6:
        st.success(f"Decrypted Message: **{decrypted}**")

    if decrypted == message:
        st.success("✅ Decryption successful! The decrypted message matches the original.")
    else:
        st.error("❌ Decryption failed.")
