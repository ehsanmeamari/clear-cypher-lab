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

    # ── Installation ─────────────────────────────────────────────────────────
    with st.expander("Installation", expanded=False):
        st.markdown("**1. Node.js**")
        st.link_button("Download Node.js", "https://nodejs.org")
        st.markdown("**2. Circom**")
        st.link_button("Download Circom", "https://github.com/iden3/circom/releases")
        st.markdown("**3. snarkjs**")
        st.code("npm install -g snarkjs", language="text")

    # ── Workflow ─────────────────────────────────────────────────────────────
    with st.expander("Workflow", expanded=False):

        st.markdown("**Step 1 — Compile Circuit**")
        st.code("./circom zkAuction.circom --r1cs --wasm", language="text")

        st.markdown("**Step 2 — Generate Witness**")
        st.code(
            "node zkAuction_js/generate_witness.js "
            "zkAuction_js/zkAuction.wasm zkAuction.input.json zkAuction.wtns",
            language="text"
        )

        st.markdown("**Step 3 — Trusted Setup**")
        st.code(
            "snarkjs powersoftau new bn128 12 tmp.ptau\n"
            "snarkjs powersoftau prepare phase2 tmp.ptau zkAuction.ptau\n"
            "rm tmp.ptau\n"
            "snarkjs groth16 setup zkAuction.r1cs zkAuction.ptau zkAuction.pk",
            language="text"
        )

        st.markdown("**Step 4 — Export Verification Key**")
        st.code(
            "snarkjs zkey export verificationkey zkAuction.pk zkAuction.vk",
            language="text"
        )

        st.markdown("**Step 5 — Proof Generation**")
        st.code(
            "snarkjs groth16 prove zkAuction.pk zkAuction.wtns zkAuction.pf zkAuction.inst",
            language="text"
        )

        st.markdown("**Step 6 — Proof Verification**")
        st.code(
            "snarkjs groth16 verify zkAuction.vk zkAuction.inst zkAuction.pf",
            language="text"
        )
