import streamlit as st

def run_modular_math():    
    """
    Renders the Modular Arithmetic tools. 
    Only the clickable header of the expanders is styled with a cream color, 
    while the expanded content remains transparent/white.
    """
    
    # Inject Custom CSS to style only the header (summary)
    st.markdown("""
        <style>
        /* 1. Target the clickable header */
        div[data-testid="stExpander"] details summary {
            background-color: #FDF5E6; /* Cream color */
            border-radius: 8px 8px 0px 0px; /* Rounded corners only at the top */
            padding: 10px;
        }

        /* 2. Remove background from the entire container to keep content clear */
        div[data-testid="stExpander"] {
            background-color: transparent !important;
            border: 1px solid #e6e6e6;
            border-radius: 8px;
        }

        /* 3. Style the content area inside the expander */
        div[data-testid="stExpander"] details > div[role="region"] {
            background-color: transparent !important;
            padding-top: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Layout: Divide the UI into two main columns
    col_left, col_right = st.columns(2)
    
    # --- Left Column: Modulo Calculator ---
    with col_left:
        with st.expander("🔢 Modulo Calculator", expanded=False):
            c1, c2, c3 = st.columns([1, 1, 1.2])
            with c1:
                val_a = st.number_input("a:", value=17, key="unique_mod_a")
            with c2:
                val_n = st.number_input("n:", value=5, key="unique_mod_n")
            with c3:
                st.markdown("<div style='margin-top:28px;'>", unsafe_allow_html=True)
                if val_n != 0:
                    st.code(f"{val_a % val_n}", language="text")
                else:
                    st.error("Error")
                st.markdown("</div>", unsafe_allow_html=True)

    # --- Right Column: Modular Inverse ---
    with col_right:
        with st.expander("🔄 Modular Inverse", expanded=False):
            i1, i2, i3 = st.columns([1, 1, 1.2])
            with i1:
                inv_a = st.number_input("a:", value=3, key="unique_inv_a")
            with i2:
                inv_n = st.number_input("n:", value=11, key="unique_inv_n")
            with i3:
                st.markdown("<div style='margin-top:28px;'>", unsafe_allow_html=True)
                try:
                    res = pow(int(inv_a), -1, int(inv_n))
                    st.code(f"{res}", language="text")
                except ValueError:
                    st.error("None")
                st.markdown("</div>", unsafe_allow_html=True)
            
            try:
                res = pow(int(inv_a), -1, int(inv_n))
                st.latex(rf"{inv_a} \times {res} \equiv 1 \pmod{{{inv_n}}}")
            except ValueError:
                pass
