import streamlit as st

def render_header_view():
    # Header Section with optimized spacing
    col_left, col_center, col_right = st.columns([1, 2.5, 1.2])

    with col_left:
        st.empty()

    with col_center:
        # Centered Logo and Professional Tagline
        st.markdown(
            """
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <img src="https://raw.githubusercontent.com/ehsanmeamari/clear-cypher-lab/main/logo.png" width="160">
                <div style="font-size: 1.3em; color: #1a365d; margin-top: 15px; font-weight: 700; text-align: center; letter-spacing: 0.5px;">
                    Demystifying the Math of Cybersecurity
                </div>
                <div style="font-size: 0.95em; color: #4a5568; margin-top: 5px; font-weight: 400; text-align: center;">
                    Interactive Learning Environment for ZKP, ECC & Blockchain
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with col_right:
        # Right-aligned Social Media Buttons
        st.markdown("""
            <div style="display: flex; flex-direction: column; align-items: flex-end; width: 100%; padding-top: 5px;">
                <div style="font-weight: bold; font-size: 0.85em; color: #555; margin-bottom: 8px; white-space: nowrap;">
                    🔗 Social Media
                </div>
                <div style="display: flex; flex-direction: column; gap: 6px; align-items: flex-end;">
                    <a href="https://www.youtube.com/@ClearCypherLab" target="_blank" style="text-decoration: none;">
                        <div style="background-color: #FF0000; color: white; padding: 6px 14px; border-radius: 4px; font-weight: bold; font-size: 0.75em; width: 105px; text-align: center;">
                            📺 YOUTUBE
                        </div>
                    </a>
                    <a href="https://www.linkedin.com/company/113012501/" target="_blank" style="text-decoration: none;">
                        <div style="background-color: #0077B5; color: white; padding: 6px 14px; border-radius: 4px; font-weight: bold; font-size: 0.75em; width: 105px; text-align: center;">
                            🔗 LINKEDIN
                        </div>
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
