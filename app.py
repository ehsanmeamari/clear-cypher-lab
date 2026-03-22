# 2. Header Section
# Using 1-3-1 ratio to give the center more room and ensure absolute centering
col_left, col_center, col_right = st.columns([1, 3, 1])

with col_left:
    st.write("") # Spacer

with col_center:
    # Centering the logo image using a div container
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; width: 100%;">
            <img src="app/static/logo.png" width="160">
        </div>
        """, 
        unsafe_allow_html=True
    )
    # Centered subtitle directly under the logo
    st.markdown('<div style="text-align: center; font-size: 1em; color: #334e68; margin-top: 10px; font-weight: 500;">Interactive Cryptography Learning Environment</div>', unsafe_allow_html=True)

with col_right:
    # Social Media pinned to the right side as shown in your layout
    st.markdown('<div style="text-align: right;">', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 5px; font-weight: bold; font-size: 0.8em; color: #555;">🔗 Social Media</p>', unsafe_allow_html=True)
    st.markdown("""
        <div style="display: flex; flex-direction: column; gap: 4px; align-items: flex-end;">
            <a href="https://www.youtube.com/@ClearCypherLab" target="_blank" style="text-decoration: none;">
                <div style="background-color: #FF0000; color: white; padding: 4px 12px; text-align: center; border-radius: 4px; font-weight: bold; font-size: 0.7em; min-width: 90px;">📺 YOUTUBE</div>
            </a>
            <a href="https://www.linkedin.com/company/113012501/" target="_blank" style="text-decoration: none;">
                <div style="background-color: #0077B5; color: white; padding: 4px 12px; text-align: center; border-radius: 4px; font-weight: bold; font-size: 0.7em; min-width: 90px;">🔗 LINKEDIN</div>
            </a>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
