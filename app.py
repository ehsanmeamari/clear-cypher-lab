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


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Clear Cypher Lab",
    page_icon="logo.png",
    layout="wide"
)

# =========================================================
# Website Header & Visitor Count
# =========================================================

render_header_view()

# Show visitor count right below header
count = get_visitor_count()
if count is not None:
    st.caption(f"👥 {count:,} unique visitors")
else:
    st.caption("👥 Visitor counter active")

# =========================================================
# Main Navigation Tabs
# =========================================================

tab1, tab2, tab3 = st.tabs(["🌐 Cryptography", "⛓️ Blockchain", "🔐 ZKP"])

with tab1:
    render_cryptography_tab()

with tab2:
    render_blockchain_tab()

with tab3:
    render_zkp_tab()
