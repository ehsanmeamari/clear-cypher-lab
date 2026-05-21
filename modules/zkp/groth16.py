import streamlit as st
import galois
import numpy as np
from py_ecc.optimized_bn128 import multiply, G1, G2, add, pairing, neg, normalize


@st.cache_resource
def get_field():
    p = 21888242871839275222246405745257275088548364400416034343698204186575808495617
    return galois.GF(p), p


def compute_commit(poly, trusted_points, FP):
    coeff = poly.coefficients()[::-1]
    if len(coeff) < len(trusted_points):
        padding = [FP(0)] * (len(trusted_points) - len(coeff))
        coeff = list(coeff) + padding
    assert len(coeff) == len(trusted_points), "Polynomial degree mismatch!"
    terms = [multiply(point, int(c)) for point, c in zip(trusted_points, coeff)]
    evaluation = terms[0]
    for i in range(1, len(terms)):
        evaluation = add(evaluation, terms[i])
    return evaluation


def run_groth16():
    FP, p = get_field()

    # ── Step 1: Inputs + Witness Vector ─────────────────────────────────────
    st.markdown("### Step 1: Circuit Inputs & Witness Vector")
    col_input, col_witness = st.columns([1, 2])

    with col_input:
        st.markdown("**Inputs**")
        c1, c2, c3 = st.columns(3)
        with c1:
            x1_val = st.number_input("x₁", value=1)
        with c2:
            x2_val = st.number_input("x₂", value=2)
        with c3:
            x3_val = st.number_input("x₃", value=2)

    x1 = FP(x1_val % p)
    x2 = FP(x2_val % p)
    x3 = FP(x3_val % p)

    v1 = x1 * x1
    v2 = x1 * x2
    v3 = x2 * v2
    y  = x2 * x3 + v1 + v2 + v3 + FP(3)

    W = FP([1, y, x1, x2, x3, v1, v2, v3])

    with col_witness:
        st.markdown("**Witness Vector W = [1, y, x₁, x₂, x₃, v₁, v₂, v₃]**")
        w_labels = ["1 (const)", "y", "x₁", "x₂", "x₃", "v₁ = x₁²", "v₂ = x₁·x₂", "v₃ = x₂·v₂"]
        w_values = list(map(int, W))
        cols = st.columns(8)
        for col, label, val in zip(cols, w_labels, w_values):
            with col:
                st.metric(label=label, value=str(val))
        st.caption(f"y = x₂·x₃ + x₁² + x₁·x₂ + x₂·(x₁·x₂) + 3 = {int(y)}")

    st.divider()

    # ── Step 2: R1CS ─────────────────────────────────────────────────────────
    st.markdown("### Step 2: Naïve protocol")

    xL = FP([[0,0,1,0,0,0,0,0],
             [0,0,1,0,0,0,0,0],
             [0,0,0,1,0,0,0,0],
             [0,0,0,1,0,0,0,0]])

    xR = FP([[0,0,1,0,0,0,0,0],
             [0,0,0,1,0,0,0,0],
             [0,0,0,0,0,0,1,0],
             [0,0,0,0,1,0,0,0]])

    xO = FP([[0,0,0,0,0,1,0,0],
             [0,0,0,0,0,0,1,0],
             [0,0,0,0,0,0,0,1],
             [FP(p-3),1,0,0,0,FP(p-1),FP(p-1),FP(p-1)]])

    with st.expander("Show Matrices: xL, xR, xO"):
        mc1, mc2, mc3 = st.columns(3)
        with mc1:
            st.markdown("**xL**")
            st.code("\n".join(str(list(map(int, row))) for row in xL))
        with mc2:
            st.markdown("**xR**")
            st.code("\n".join(str(list(map(int, row))) for row in xR))
        with mc3:
            st.markdown("**xO**")
            st.code("\n".join(str(list(map(int, row))) for row in xO))

    xLWT = np.dot(xL, W)
    xRWT = np.dot(xR, W)
    xOWT = np.dot(xO, W)
    xLWTxRWT = np.multiply(xLWT, xRWT)

    col_l, col_r, col_o = st.columns(3)
    with col_l:
        st.markdown("**xL · W**")
        st.code(str(list(map(int, xLWT))))
    with col_r:
        st.markdown("**xR · W**")
        st.code(str(list(map(int, xRWT))))
    with col_o:
        st.markdown("**xO · W**")
        st.code(str(list(map(int, xOWT))))

    if not np.all(xLWTxRWT == xOWT):
        st.error("❌ R1CS verification failed.")
        return
    st.success("✅ (xL·W) ∘ (xR·W) = xO·W — R1CS passed!")
    st.divider()

    # ── Step 3: QAP ──────────────────────────────────────────────────────────
    st.markdown("### Step 3: QAP — Lagrange Interpolation")

    with st.spinner("Computing polynomials..."):
        poly_m = []
        for m in [xL, xR, xO]:
            poly_list = []
            for i in range(m.shape[1]):
                px = FP(np.zeros(m.shape[0], dtype=int))
                py = FP(np.zeros(m.shape[0], dtype=int))
                for j in range(m.shape[0]):
                    px[j] = FP(j + 1)
                    py[j] = m[j][i]
                poly = galois.lagrange_poly(px, py)
                coef = poly.coefficients()[::-1]
                if len(coef) < m.shape[0]:
                    coef = np.append(coef, np.zeros(m.shape[0] - len(coef), dtype=int))
                poly_list.append(coef)
            poly_m.append(FP(poly_list))

    L_polys, R_polys, O_polys = poly_m

    Lx = galois.Poly((W @ L_polys)[::-1])
    Rx = galois.Poly((W @ R_polys)[::-1])
    Ox = galois.Poly((W @ O_polys)[::-1])

    Tx = galois.Poly([1, p - 1], field=FP)
    for i in range(2, xL.shape[0] + 1):
        Tx *= galois.Poly([1, p - i], field=FP)

    Hx  = (Lx * Rx - Ox) // Tx
    rem = (Lx * Rx - Ox) % Tx

    st.code(f"L(x) = {Lx}\nR(x) = {Rx}\nO(x) = {Ox}\nT(x) = {Tx}\nH(x) = {Hx}")

    if rem != 0:
        st.error(f"❌ Remainder is not zero: {rem}")
        return
    st.success("✅ L(x)·R(x) − O(x) = H(x)·T(x)  (remainder = 0)")
    st.divider()

    # ── Step 4: Setup ────────────────────────────────────────────────────────
    st.markdown("### Step 4: Trusted Setup (SRS Generation)")
    tau_val = st.slider("Toxic waste τ", min_value=2, max_value=100, value=20)
    tau = FP(tau_val)

    with st.spinner("Computing SRS on BN128 curve..."):
        Tx_tau  = Tx(tau)
        Lx_tau  = Lx(tau)
        Rx_tau  = Rx(tau)
        Ox_tau  = Ox(tau)
        Hx_tau  = Hx(tau)
        HTx_tau = Hx_tau * Tx_tau

        SRS_G1      = [multiply(G1, int(tau**i)) for i in range(Tx.degree)]
        SRS_G2      = [multiply(G2, int(tau**i)) for i in range(Tx.degree)]
        SRS_Ttau_G1 = [multiply(G1, int(tau**i * Tx_tau)) for i in range(Tx.degree - 1)]

    if Lx_tau * Rx_tau != Ox_tau + HTx_tau:
        st.error("❌ Tau check failed.")
        return
    st.success(f"✅ L(τ)·R(τ) = O(τ) + H(τ)·T(τ)  (τ = {tau_val})")

    with st.expander("Show SRS points"):
        st.markdown("**SRS_G1**")
        st.code("\n".join(str(normalize(pt)) for pt in SRS_G1))
        st.markdown("**SRS_G2**")
        st.code("\n".join(str(normalize(pt)) for pt in SRS_G2))
        st.markdown("**SRS_Ttau_G1**")
        st.code("\n".join(str(normalize(pt)) for pt in SRS_Ttau_G1))
    st.divider()

    # ── Step 5: Proof ────────────────────────────────────────────────────────
    st.markdown("### Step 5: Proof Generation")

    with st.spinner("Computing commitments..."):
        Com_L_G1       = compute_commit(Lx, SRS_G1, FP)
        Com_R_G2       = compute_commit(Rx, SRS_G2, FP)
        Com_O_G1       = compute_commit(Ox, SRS_G1, FP)
        Com_H_TG1      = compute_commit(Hx, SRS_Ttau_G1, FP)
        Com_O_G1_H_TG1 = add(Com_O_G1, Com_H_TG1)

    st.code(
        f"Com_L_G1       = {normalize(Com_L_G1)}\n"
        f"Com_R_G2       = {normalize(Com_R_G2)}\n"
        f"Com_O_G1       = {normalize(Com_O_G1)}\n"
        f"Com_H_TG1      = {normalize(Com_H_TG1)}\n"
        f"Com_O_G1_H_TG1 = {normalize(Com_O_G1_H_TG1)}"
    )
    st.divider()

    # ── Step 6: Verify ───────────────────────────────────────────────────────
    st.markdown("### Step 6: Proof Verification")

    with st.spinner("Computing pairing..."):
        lhs = pairing(Com_R_G2, Com_L_G1)
        rhs = pairing(G2, Com_O_G1_H_TG1)

    st.code(
        f"pairing(Com_R_G2, Com_L_G1)        = {lhs}\n"
        f"pairing(G2, Com_O_G1 + Com_H_TG1)  = {rhs}"
    )

    if lhs == rhs:
        st.success("✅ Pairing check passed!  e(Com_L, Com_R) = e(G2, Com_O + Com_H·T)")
    else:
        st.error("❌ Pairing check failed.")
