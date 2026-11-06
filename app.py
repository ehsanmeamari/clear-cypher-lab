
import streamlit as st
import requests

from modules.zkp.styles import apply_styles

from views.header_view import render_header_view
from views.computer_view import render_computer_tab
from views.cryptography_view import render_cryptography_tab
from views.blockchain_view import render_blockchain_tab
from views.zkp_view import render_zkp_tab


# =========================================================
# Visitor Counter
# =========================================================

def get_visitor_count():
    try:
        auth = requests.post(
            "http://localhost:3000/api/auth/login",
            json={
                "username": "admin",
                "password": "umami"
            },
            timeout=3
        )

        auth.raise_for_status()
        token = auth.json()["token"]

        stats = requests.get(
            "http://localhost:3000/api/websites/1f6c16b1-f990-4972-85d9-a691bd71badd/stats",
            headers={
                "Authorization": f"Bearer {token}"
            },
            params={
                "startAt": 0,
                "endAt": 9999999999999
            },
            timeout=3
        )

        stats.raise_for_status()

        return stats.json()["visitors"]

    except Exception:
        return None


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Clear Cypher Lab",
    page_icon="logo.png",
    layout="wide"
)


# =========================================================
# Umami Analytics
# =========================================================

st.markdown("""
    <script defer
        src="https://analytics.clearcypherlab.com/script.js"
        data-website-id="1f6c16b1-f990-4972-85d9-a691bd71badd">
    </script>
""", unsafe_allow_html=True)


# =========================================================
# Global CSS
# =========================================================

st.markdown("""
    <style>

        /* Hide Streamlit Header */
        header[data-testid="stHeader"] {
            display: none !important;
        }

        /* Main Container */
        .main .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            margin-top: -45px !important;
        }

        /* Compact Vertical Spacing */
        [data-testid="stVerticalBlock"] > div {
            gap: 0.1rem !important;
        }

        /* Hide Settings and Footer */
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        /* Navigation Buttons */
        div.stButton > button {
            height: 40px !important;
            border-radius: 6px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease-in-out;
        }

        /* Navigation Hover */
        div.stButton > button:hover {
            border-color: #269e9b !important;
            color: #269e9b !important;
        }

        /* Active Navigation Button */
        div.stButton > button[kind="primary"] {
            background-color: #269e9b !important;
            border-color: #269e9b !important;
            color: white !important;
        }

        /* Navigation Layout */
        [data-testid="stHorizontalBlock"] {
            gap: 8px !important;
        }

    </style>
""", unsafe_allow_html=True)


# =========================================================
# Apply Custom Styles
# =========================================================

apply_styles()


# =========================================================
# Website Header
# =========================================================

render_header_view()


# =========================================================
# Visitor Count
# =========================================================

count = get_visitor_count()

if count is not None:
    st.caption(f"👥 {count:,} unique visitors")


# =========================================================
# Main Navigation State
# =========================================================

if "active_section" not in st.session_state:
    st.session_state.active_section = None


# =========================================================
# Main Navigation Menu
# =========================================================

st.markdown("""
    <style>
        .navigation-label {
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 5px;
        }
    </style>
""", unsafe_allow_html=True)


nav1, nav2, nav3, nav4 = st.columns(5)


with nav1:
    if st.button(
        "💻 Computer",
        key="nav_computer",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.active_section == "Computer"
            else "secondary"
        )
    ):
        st.session_state.active_section = "Computer"
        st.rerun()


with nav2:
    if st.button(
        "🌐 Cryptography",
        key="nav_cryptography",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.active_section == "Cryptography"
            else "secondary"
        )
    ):
        st.session_state.active_section = "Cryptography"
        st.rerun()


with nav3:
    if st.button(
        "⛓️ Blockchain",
        key="nav_blockchain",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.active_section == "Blockchain"
            else "secondary"
        )
    ):
        st.session_state.active_section = "Blockchain"
        st.rerun()


with nav4:
    if st.button(
        "🔐 ZKP",
        key="nav_zkp",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.active_section == "ZKP"
            else "secondary"
        )
    ):
        st.session_state.active_section = "ZKP"
        st.rerun()

with nav5:
    
# =========================================================
# Navigation Divider
# =========================================================

st.divider()


# =========================================================
# Render Selected Section
# =========================================================

active_section = st.session_state.active_section


if active_section == "Computer":

    render_computer_tab()


elif active_section == "Cryptography":

    render_cryptography_tab()


elif active_section == "Blockchain":

    render_blockchain_tab()


elif active_section == "ZKP":

    render_zkp_tab()


else:

    st.markdown("""
        <div style="
            text-align: center;
            padding: 65px 15px;
            color: #888888;
        ">
            <div style="font-size: 42px; margin-bottom: 15px;">
                🧪
            </div>

            <div style="
                font-size: 20px;
                font-weight: 600;
                margin-bottom: 8px;
            ">
                Welcome to Clear Cypher Lab
            </div>

            <div style="font-size: 14px;">
                Select a section to get started.
            </div>
        </div>
    """, unsafe_allow_html=True)


# =========================================================
# Footer Divider
# =========================================================

st.divider()
