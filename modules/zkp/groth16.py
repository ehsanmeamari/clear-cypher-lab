# ── Step 1: Inputs + Witness Vector ─────────────────────────────────────
    st.markdown("### Step 1: Circuit Inputs & Witness Vector")
    col_input, col_witness = st.columns(2)

    with col_input:
        st.markdown("**Inputs**")
        x1_val = st.number_input("x₁", min_value=0, max_value=100, value=1, step=1)
        x2_val = st.number_input("x₂", min_value=0, max_value=100, value=2, step=1)
        x3_val = st.number_input("x₃", min_value=0, max_value=100, value=2, step=1)

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
        row1 = st.columns(4)
        row2 = st.columns(4)
        for i, (label, val) in enumerate(zip(w_labels, w_values)):
            col = row1[i] if i < 4 else row2[i - 4]
            with col:
                st.metric(label=label, value=str(val))
        st.caption(f"y = x₂·x₃ + x₁² + x₁·x₂ + x₂·(x₁·x₂) + 3 = {int(y)}")

    st.divider()
