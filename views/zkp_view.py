import streamlit as st
from modules.ecc_tool import run_ecc_visualizer
from modules.modular_math import run_modular_math
from modules.ecc_math import ecc_fp

def render_zkp_tab():
    # CSS متعادل شده برای ظاهر پرتر
    st.markdown("""
        <style>
            /* کاهش شدت منفی بودن مارجین برای جلوگیری از "خالی" دیده شدن پایین صفحه */
            div[data-testid="stRadio"] { margin-top: -10px !important; margin-bottom: 10px !important; }
            /* ایجاد فضای مناسب برای جداکننده‌ها */
            hr { margin-top: 10px !important; margin-bottom: 15px !important; opacity: 0.2; }
            /* افزایش فاصله بین المان‌های عمودی برای پر شدن بصری صفحه */
            [data-testid="stVerticalBlock"] > div { gap: 1rem !important; }
        </style>
        """, unsafe_allow_html=True)

    # --- 1. Primary Protocol Selection ---
    zkp_protocol = st.radio(
        label="Protocol", 
        options=["Groth16", "Plonk", "Spartan", "Nova"], 
        key="zkp_p", 
        horizontal=True, 
        label_visibility="collapsed"
    )
    st.divider()

    if zkp_protocol == "Groth16":
        # --- 2. Module Selection for Groth16 ---
        zkp_module = st.radio(
            label="Module", 
            options=["Modular Arithmetic", "Extension Field", "ECC", "Weil Pairing", "Lagrange Interpolation"], 
            key="g16_m", 
            horizontal=True, 
            label_visibility="collapsed"
        )
        st.divider()
        
        if zkp_module == "Modular Arithmetic":
            run_modular_math()
            
        elif zkp_module == "Extension Field":
            st.info("Extension Field logic is coming soon.")
        
        elif zkp_module == "ECC":
            # --- 3. ECC Sub-module Selection ---
            ecc_sub = st.radio(
                label="ECC Sub", 
                options=[
                    "Visualizer over R", "Addition over R", "Multiplication over R", 
                    "Visualizer over Fp", "Addition over Fp", "Multiplication over Fp"
                ], 
                key="ecc_s", 
                horizontal=True, 
                label_visibility="collapsed"
            )
            st.divider()
            
            if ecc_sub == "Addition over Fp":
                # فراخوانی تابع اصلی
                ecc_fp()
            elif ecc_sub == "Visualizer over R":
                run_ecc_visualizer()
            else:
                st.info(f"{ecc_sub} logic is coming soon.")

        elif zkp_module == "Weil Pairing":
            st.info("Weil Pairing logic is coming soon.")

        elif zkp_module == "Lagrange Interpolation":
            st.info("Lagrange Interpolation logic is coming soon.")
