import streamlit as st
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def aes_ui():
    col1, col2 = st.columns(2)
    with col1:
        mode = st.selectbox("Key Size", ["AES-128 (16 bytes)", "AES-192 (24 bytes)", "AES-256 (32 bytes)"])
        key_size = int(mode.split("(")[1].split(" ")[0])
        aes_mode = st.selectbox("Mode", ["ECB", "CBC"])
        key_input = st.text_input("Key (hex):", value="00" * key_size)
        iv_input = None
        if aes_mode == "CBC":
            iv_input = st.text_input("IV (hex):", value="00" * 16)
        plaintext = st.text_area("Plaintext:", value="Hello, AES World!", height=100)
        encrypt_btn = st.button("Encrypt", use_container_width=True)
    with col2:
        ciphertext_input = st.text_area("Ciphertext (base64):", height=100)
        decrypt_btn = st.button("Decrypt", use_container_width=True)
    try:
        key_bytes = bytes.fromhex(key_input)
        if len(key_bytes) != key_size:
            st.error(f"Key must be exactly {key_size*2} hex characters.")
            return
    except ValueError:
        st.error("Key must be valid hex.")
        return
    iv_bytes = None
    if aes_mode == "CBC" and iv_input:
        try:
            iv_bytes = bytes.fromhex(iv_input)
            if len(iv_bytes) != 16:
                st.error("IV must be exactly 32 hex characters.")
                return
        except ValueError:
            st.error("IV must be valid hex.")
            return
    if encrypt_btn:
        try:
            padded = pad(plaintext.encode('utf-8'), AES.block_size)
            cipher = AES.new(key_bytes, AES.MODE_ECB) if aes_mode == "ECB" else AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
            encrypted = cipher.encrypt(padded)
            with st.expander("Encryption Result", expanded=True):
                st.markdown("**Base64:**")
                st.code(base64.b64encode(encrypted).decode('utf-8'))
                st.markdown("**Hex:**")
                st.code(encrypted.hex())
        except Exception as e:
            st.error(f"Encryption error: {e}")
    if decrypt_btn:
        try:
            encrypted_bytes = base64.b64decode(ciphertext_input.strip())
            cipher = AES.new(key_bytes, AES.MODE_ECB) if aes_mode == "ECB" else AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
            decrypted = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
            with st.expander("Decryption Result", expanded=True):
                st.markdown("**Plaintext:**")
                st.code(decrypted.decode('utf-8'))
        except Exception as e:
            st.error(f"Decryption error: {e}")
