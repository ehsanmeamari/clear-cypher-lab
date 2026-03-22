import streamlit as st
from modules.ecc_tool import run_ecc_visualizer
from modules.modular_math import run_modular_math
# اضافه کردن ایمپورت جدید برای بخش ریاضیات ECC
from modules.ecc_math import ecc_fp

def render_zkp_tab():
    # CSS to reduce vertical gaps globally in this tab
    st.markdown("""
        <style>
            div[data-testid="stRadio"] { margin-top: -20px !important; }
            hr { margin-top: 5px !important; margin-bottom: 10px !important; }
            [data-testid="stVerticalBlock"] > div { gap: 0.5rem !important; }
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
            
            if ecc_sub == "Visualizer over R":
                run_ecc_visualizer()
            
            elif ecc_sub == "Addition over Fp":
                # فراخوانی تابع از فایل ecc_math.py
                ecc_fp()
                
            else:
                st.info(f"{ecc_sub} logic is coming soon.")
        else:
            st.info(f"{zkp_module} for Groth16 is under development.")

    elif zkp_protocol == "Plonk":
        # ... (بقیه کد بدون تغییر باقی می‌ماند)
        plonk_sub = st.radio(
            label="Plonk Sub", 
            options=["Tate Pairing", "KZG Commitment Scheme"], 
            key="plonk_s", 
            horizontal=True, 
            label_visibility="collapsed"
        )
        st.divider()
        st.info(f"{plonk_sub} module for Plonk is coming soon.")
    
    # ... (بقیه کد)
