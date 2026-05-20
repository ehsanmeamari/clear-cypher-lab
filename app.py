import streamlit as st
import requests
from modules.zkp.styles import apply_styles
from views.header_view import render_header_view
from views.cryptography_view import render_cryptography_tab
from views.blockchain_view import render_blockchain_tab
from views.zkp_view import render_zkp_tab

def get_visitor_count():
    try:
        auth = requests.post("http://localhost:3000/api/auth/login",
            json={"username": "admin", "password": "umami"})
        token = auth.json()["token"]
        stats = requests.get(
            "http://localhost:3000/api/websites/1f6c16b1-f990-4972-85d9-a691bd71badd/stats",
            headers={"Authorization": f"Bearer {token}"},
            params={"startAt": 0, "endAt": 9999999999999}
        )
        return stats.json()["visitors"]
    except:
        return None

# Initial page configuration
st.set_page_config(
    page_title="Clear Cypher Lab", 
    page_icon="logo.png", 
    layout="wide"
)

# Umami Analytics
st.markdown("""
    <script defer src="https://analytics.clearcypherlab.com/script.js" 
    data-website-id="1f6c16b1-f990-4972-85d9-a691bd71badd"></script>
""", unsafe_allow_html=True)

# Aggressively remove default header and extra padding
st.markdown("""
    <style>
        /* Hide Streamlit's top header bar */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        /* Remove main body padding and pull content to the top */
        .main .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            margin-top: -45px !important; /* Compensate for system whitespace */
        }
        /* Remove automatic gap between widgets for compact layout */
        [data-testid="stVerticalBlock"] > div {
            gap: 0.1rem !important;
        }
        /* Hide settings menu and footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Adjust tab height for a cleaner look */
        button[data-baseweb="tab"] {
            height: 40px !important;
            padding-top: 0px !important;
            padding-bottom: 0px !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Apply custom side padding styles
apply_styles()

# Render site header
render_header_view()

# Show visitor count
count = get_visitor_count()
if count is not None:
    st.caption(f"👥 {count:,} unique visitors")

# Create main navigation tabs
tab1, tab2, tab3 = st.tabs(["🌐 Cryptography", "⛓️ Blockchain", "🔐 ZKP"])

with tab1: 
    render_cryptography_tab()
with tab2: 
    render_blockchain_tab()
with tab3: 
    render_zkp_tab()

st.divider()
