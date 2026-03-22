import streamlit as st
from modules.styles import apply_styles
from modules.ecc_tool import run_ecc_visualizer

# 1. Page Configuration
st.set_page_config(page_title="Clear Cypher Lab", page_icon="🛡️", layout="wide")
apply_styles()

# 2. RTL (Right-to-Left) Custom CSS
st.markdown(
    """
    <style>
    .main {
        direction: rtl;
        text-align: right;
    }
    div[data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }
    div[data-testid="stMarkdownContainer"] p {
        text-align: right;
    }
    /* Fixing Radio and Selectbox alignment for RTL */
    div.row-widget.stRadio > div {
        flex-direction: row-reverse;
        justify-content: flex-end;
    }
    div[data-testid="stExpander"] {
        direction: rtl;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Sidebar Navigation
with st.sidebar:
    st.title("🛡️ Clear Cypher Lab")
    st.markdown("---")
    st.write("🔗 **Social Media:**")
    
    col_yt, col_li = st.columns(2)
    with col_yt:
        st.markdown(
            """<a href="https://www.youtube.com/@ClearCypherLab" target="_blank">
            <img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" width="100%"></a>""", 
            unsafe_allow_html=True)
    with col_li:
        st.markdown(
            """<a href="https://www.linkedin.com/company/113012501/" target="_blank">
            <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" width="100%"></a>""", 
            unsafe_allow_html=True)
    st.markdown("---")

# 4. Main Content
st.title("🛡️ Clear Cypher Lab")
st.markdown("Interactive Cryptography Learning Environment")

tab1, tab2, tab3 = st.tabs(["🌐 Cryptography", "⛓️ Blockchain", "🔐 ZKP"])

with tab1:
    st.header("Cryptography")
    st.info("🚀 Advanced cryptography modules are under development.")

with tab2:
    st.header("Blockchain Infrastructure")
    st.info("🚀 Blockchain simulation tools coming soon.")

with tab3:
    st.header("Zero-Knowledge Proofs (ZKP)")
    
    # Main ZKP Navigation (Label Hidden)
    zkp_module = st.radio(
        label="Select a Module:",
        options=["Modular Arithmetic", "Extension Field", "ECC", "Weil Pairing", "Lagrange Interpolation"], 
        key="zkp_main",
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.divider()

    if zkp_module == "Modular Arithmetic":
        st.subheader("Modular Arithmetic")
        
        # Horizontal sub-menu
        mod_sub_module = st.radio(
            label="Sub Operation:",
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
                num_a = st.number_input("Enter a:", value=17, key="mod_calc_a")
            with col2:
                num_n = st.number_input("Enter n:", value=5, key="mod_calc_n")
            
            if num_n != 0:
                st.code(f"{num_a} mod {num_n} = {num_a % num_n}", language="text")
            else:
                st.error("Modulo by zero is undefined!")

        elif mod_sub_module == "Modular Inverse":
            st.write("### 🔄 Modular Multiplicative Inverse")
            col1, col2 = st.columns(2)
            with col1:
                inv_a = st.number_input("Enter a:", value=3, key="inv_a")
            with col2:
                inv_n = st.number_input("Enter n:", value=11, key="inv_n")
            try:
                res_inv = pow(int(inv_a), -1, int(inv_n))
                st.success(f"Result: {res_inv}")
                st.latex(f"{inv_a} \\cdot {res_inv} \\equiv 1 \\pmod{{{inv_n}}}")
            except ValueError:
                st.error("Inverse does not exist.")

    elif zkp_module == "Extension Field":
        st.subheader("Extension Field")
        st.info("Coming soon.")
        
    elif zkp_module == "ECC":
        ecc_sub = st.selectbox("ECC Operations:", ["Visualizer", "Point Addition", "Scalar Multiplication"])
        if ecc_sub == "Visualizer":
            run_ecc_visualizer()
        else:
            st.info(f"{ecc_sub} tool is under development.")

    elif zkp_module == "Weil Pairing":
        st.subheader("Weil Pairing")
        st.info("Coming soon.")

    elif zkp_module == "Lagrange Interpolation":
        st.subheader("Lagrange Interpolation")
        st.info("Coming soon.")

st.divider()
