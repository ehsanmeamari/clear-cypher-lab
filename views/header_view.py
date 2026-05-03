import streamlit as st

def render_header_view():
    # Internal styles for header spacing and horizontal rule
    st.markdown("""
        <style>
            .header-wrapper { margin-top: 5px; padding-bottom: 0px; }
            .custom-hr { margin-top: 5px !important; margin-bottom: 10px !important; opacity: 0.15; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="header-wrapper">', unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 2.5, 1.2])

    with col_center:
        # Central Logo and Slogan
        st.markdown(
            """
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <img src="https://raw.githubusercontent.com/ehsanmeamari/clear-cypher-lab/main/logo.png" width="150">
                <div style="font-size: 1.25em; color: #1a365d; margin-top: 8px; font-weight: 700; text-align: center;">
                    Demystifying the Math of Cybersecurity
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with col_right:
        # Social Media buttons container
        st.markdown("""
            <div style="display: flex; flex-direction: column; align-items: flex-end; width: 100%; padding-top: 10px;">
                <div style="font-weight: bold; font-size: 0.8em; color: #555; margin-bottom: 5px;">🔗 Social Media</div>
                <div style="display: flex; flex-direction: column; gap: 4px; align-items: flex-end;">
                    <a href="https://www.youtube.com/@ClearCypherLab" target="_blank" style="text-decoration: none;">
                        <div style="background-color: #FF0000; color: white; padding: 5px 12px; border-radius: 4px; font-weight: bold; font-size: 0.7em; width: 95px; text-align: center;">📺 YOUTUBE</div>
                    </a>
                    <a href="https://www.linkedin.com/company/113012501/" target="_blank" style="text-decoration: none;">
                        <div style="background-color: #0077B5; color: white; padding: 5px 12px; border-radius: 4px; font-weight: bold; font-size: 0.7em; width: 95px; text-align: center;">🔗 LINKEDIN</div>
                    </a>
                    <a href="https://github.com/ehsanmeamari/clear-cypher-lab" target="_blank" style="text-decoration: none;">
                        <div style="background-color: #24292e; color: white; padding: 5px 12px; border-radius: 4px; font-weight: bold; font-size: 0.7em; width: 95px; text-align: center;">💻 GITHUB</div>
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<hr class="custom-hr">', unsafe_allow_html=True)
