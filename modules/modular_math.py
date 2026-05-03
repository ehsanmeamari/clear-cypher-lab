import streamlit as st

def run_modular_math():    
    """
    Renders the Modular Arithmetic tools including a Modulo Calculator 
    and a Modular Inverse Calculator with customized cream-colored headers.
    """
    
    # Inject Custom CSS to change the background color of expander headers to Cream
    st.markdown("""
        <style>
        /* Target the expander container */
        div[data-testid="stExpander"] {
            background-color: #FDF5E6; /* OldLace cream color */
            border: 1px solid #e6e6e6;
            border-radius: 8px;
        }
        
        /* Ensure the click-surface of the header also maintains the background */
        div[data-testid="stExpander"] details summary {
            background-color: #FDF5E6;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Layout: Divide the UI into two main columns
    col_left, col_right = st.columns(2)
    
    # --- Left Column: Modulo Calculator ---
    with col_left:
        # 'expanded=False' ensures the section is collapsed by default upon loading
        with st.expander("🔢 Modulo Calculator", expanded=False):
            # Inner columns for inputs and result
            c1, c2, c3 = st.columns([1, 1, 1.2])
            with c1:
                val_a = st.number_input("a:", value=17, key="unique_mod_a")
            with c2:
                val_n = st.number_input("n:", value=5, key="unique_mod_n")
            with c3:
                # Vertical alignment fix for the result box
                st.markdown("<div style='margin-top:28px;'>", unsafe_allow_html=True)
                if val_n != 0:
                    st.code(f"{val_a % val_n}", language="text")
                else:
                    st.error("Error")
                st.markdown("</div>", unsafe_allow_html=True)

    # --- Right Column: Modular Inverse ---
    with col_right:
        with st.expander("🔄 Modular Inverse", expanded=False):
            # Inner columns for inputs and result
            i1, i2, i3 = st.columns([1, 1, 1.2])
            with i1:
                inv_a = st.number_input("a:", value=3, key="unique_inv_a")
            with i2:
                inv_n = st.number_input("n:", value=11, key="unique_inv_n")
            with i3:
                # Vertical alignment fix for the result box
                st.markdown("<div style='margin-top:28px;'>", unsafe_allow_html=True)
                try:
                    # Calculate modular multiplicative inverse
                    res = pow(int(inv_a), -1, int(inv_n))
                    st.code(f"{res}", language="text")
                except ValueError:
                    # Error handling if the inverse does not exist
                    st.error("None")
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Display the mathematical verification formula using LaTeX
            try:
                res = pow(int(inv_a), -1, int(inv_n))
                st.latex(rf"{inv_a} \times {res} \equiv 1 \pmod{{{inv_n}}}")
            except ValueError:
                pass
