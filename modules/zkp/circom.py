import streamlit as st


def run_circom():

    st.markdown("""
        <style>
        div[data-testid="stExpander"] details summary {
            background-color: #FDF5E6;
            border-radius: 5px;
            padding: 10px;
        }
        div[data-testid="stExpander"] {
            border: 1px solid #e6e6e6;
            border-radius: 5px;
            background-color: transparent;
        }
        div[data-testid="stExpander"] div[data-testid="stExpanderDetails"] {
            padding: 15px;
            min-height: 60px;
        }
        </style>
    """, unsafe_allow_html=True)

    # ── Colab ────────────────────────────────────────────────────────────────
    with st.expander("Colab", expanded=True):
        st.markdown(
            """
<a href="https://colab.research.google.com/github/ehsanmeamari/clear-cypher-lab/blob/main/modules/zkp/zkAuction.ipynb" target="_blank">
<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>
<span style="margin-left:8px; font-weight:bold;">zkAuction</span>
<br><br>
<a href="https://colab.research.google.com/github/ehsanmeamari/clear-cypher-lab/blob/main/modules/zkp/zkCredit.ipynb" target="_blank">
<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>
<span style="margin-left:8px; font-weight:bold;">zkCredit</span>
""",
            unsafe_allow_html=True,
        )

    # ── Installation ─────────────────────────────────────────────────────────
    with st.expander("Installation", expanded=False):
        st.markdown("""
**1. Node.js**
""")
        st.link_button("Download Node.js", "https://nodejs.org")

        st.markdown("""
**2. Circom**
""")
        st.link_button("Download Circom", "https://github.com/iden3/circom/releases")

        st.markdown("""
**3. snarkjs**
""")
        st.code("npm install -g snarkjs", language="bash")

    # ── Workflow ─────────────────────────────────────────────────────────────
    with st.expander("Workflow", expanded=False):
        st.markdown("**Step 1 — Compile Circuit**")
        st.code("circom zkAuction.circom --r1cs --wasm --sym", language="bash")

        st.markdown("**Step 2 — Generate Witness**")
        st.code("node zkAuction_js/generate_witness.js zkAuction_js/zkAuction.wasm zkAuction.input.json zkAuction.wtns", language="bash")

        st.markdown("**Step 3 — Trusted Setup**")
        st.code("""snarkjs powersoftau new bn128 12 pot12_0000.ptau
snarkjs powersoftau contribute pot12_0000.ptau pot12_0001.ptau
snarkjs powersoftau prepare phase2 pot12_0001.ptau pot12_final.ptau
snarkjs groth16 setup zkAuction.r1cs pot12_final.ptau zkAuction_0000.zkey
snarkjs zkey contribute zkAuction_0000.zkey zkAuction.zkey""", language="bash")

        st.markdown("**Step 4 — Generate & Verify Proof**")
        st.code("""snarkjs groth16 prove zkAuction.zkey zkAuction.wtns zkAuction.pf zkAuction.inst
snarkjs groth16 verify zkAuction.vk zkAuction.inst zkAuction.pf""", language="bash")
