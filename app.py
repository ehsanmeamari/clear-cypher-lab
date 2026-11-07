import streamlit as st
import requests

from modules.zkp.styles import apply_styles
from views.header_view import render_header_view
from views.computer_view import render_computer_tab
from views.cryptography_view import render_cryptography_tab
from views.blockchain_view import render_blockchain_tab
from views.zkp_view import render_zkp_tab


def get_visitor_count():
    try:
        auth = requests.post("http://localhost:3000/api/auth/login",
            json={"username": "admin", "password": "umami"}, timeout=2)
        if auth.status_code == 200:
            token = auth.json().get("token")
            stats = requests.get(
                "http://localhost:3000/api/websites/1f6c16b1-f990-4972-85d9-a691bd71badd/stats",
                headers={"Authorization": f"Bearer {token}"},
                params={"startAt": 0, "endAt": 9999999999999},
                timeout=2
            )
            if stats.status_code == 200:
                data = stats.json()
                if "visitors" in data:
                    v = data["visitors"]
                    return v.get("value") if isinstance(v, dict) else v
    except Exception as e:
        print(f"Error fetching stats: {e}")
    return None


st.set_page_config(
    page_title="Clear Cypher Lab",
    page_icon="logo.png",
    layout="wide"
)

render_header_view()

count = get_visitor_count()
if count is not None:
    st.caption(f"👥 Unique Visitors: {count:,}")
else:
    st.caption("👥 Unique Visitors: 350+")

tab1, tab2, tab3, tab4 = st.tabs(["💻 Computer", "🌐 Cryptography", "⛓️ Blockchain", "🔐 ZKP"])

with tab1:
    render_computer_tab()

with tab2:
    render_cryptography_tab()

with tab3:
    render_blockchain_tab()

with tab4:
    render_zkp_tab()
