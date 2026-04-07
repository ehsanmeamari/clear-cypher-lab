import streamlit as st
from sympy import symbols, simplify, expand
import matplotlib.pyplot as plt

# --- 1. MATHEMATICAL CORE: LAGRANGE INTERPOLATION ---

def lagrange_basis_real(x_coordinates, j):
    """ Computes the j-th Lagrange basis polynomial over Real numbers """
    x = symbols('x')
    basis = 1
    for m in range(len(x_coordinates)):
        if m != j:
            # Formula: Product of (x - xm) / (xj - xm)
            basis *= (x - x_coordinates[m]) / (x_coordinates[j] - x_coordinates[m])
    return simplify(basis)

def lagrange_real_calc(x_coords, y_coords):
    """ Computes the full interpolation polynomial f(x) over Real numbers """
    res = 0
    for i in range(len(y_coords)):
        res += lagrange_basis_real(x_coords, i) * y_coords[i]
    return expand(res)

def lagrange_basis_modp(x_coordinates, j, p):
    """ Computes the j-th Lagrange basis polynomial over Finite Field Fp """
    x = symbols('x')
    basis = 1
    for m in range(len(x_coordinates)):
        if m != j:
            # In Fp, division is multiplication by modular inverse
            denominator = int(x_coordinates[j] - x_coordinates[m])
            den_inv = pow(denominator, -1, p)
            basis *= (x - x_coordinates[m]) * den_inv
    return basis

def lagrange_mod_p_calc(x_coords, y_coords, p):
    """ Computes the full interpolation polynomial f(x) modulo p """
    res = 0
    for i in range(len(y_coords)):
        res += lagrange_basis_modp(x_coords, i, p) * y_coords[i]
    return simplify(res % p)

# --- 2. UI MODULES FOR STREAMLIT ---

def lagrange_real_ui():
    """ UI for Lagrange Interpolation over Real Numbers """
    st.subheader("📈 Lagrange Interpolation over $\mathbb{R}$")
    x_coords, y_coords = [], []
    col1, col2 = st.columns([7, 5])

    with col1:
        num_points = st.number_input("Number of points:", min_value=2, value=3, key="re_num")
        for i in range(num_points):
            c1, c2 = st.columns(2)
            with c1: x = st.number_input(f"X{i+1}:", value=float(i), key=f"rx{i}")
            with c2: y = st.number_input(f"Y{i+1}:", value=float(i**2), key=f"ry{i}")
            x_coords.append(x)
            y_coords.append(y)

        if len(set(x_coords)) != len(x_coords):
            st.error("Error: X coordinates must be distinct.")
        else:
            poly = lagrange_real_calc(x_coords, y_coords)
            with st.expander("Resulting Polynomial f(x)", expanded=True):
                st.latex(f"f(x) = {poly}")

    with col2:
        with st.expander("📊 Visualization", expanded=True):
            fig, ax = plt.subplots()
            ax.scatter(x_coords, y_coords, color='#3498db')
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)

def lagrange_fp_ui():
    """ UI for Lagrange Interpolation over Finite Fields (Fp) """
    st.subheader("🔢 Lagrange Interpolation over $\mathbb{F}_p$")
    x_coords, y_coords = [], []
    col1, col2 = st.columns([7, 5])

    with col1:
        p = st.number_input("Prime number (p):", min_value=2, value=7, key="fp_p")
        num_points = st.number_input("Number of points:", min_value=2, value=3, key="fp_num")
        for i in range(num_points):
            c1, c2 = st.columns(2)
            with c1: x = st.number_input(f"X{i+1}:", value=i, key=f"fpx{i}") % p
            with c2: y = st.number_input(f"Y{i+1}:", value=(i+1)%p, key=f"fpy{i}") % p
            x_coords.append(x)
            y_coords.append(y)

        if len(set(x_coords)) != len(x_coords):
            st.error("Error: X coordinates must be unique in $\mathbb{F}_p$.")
        else:
            poly_mod = lagrange_mod_p_calc(x_coords, y_coords, p)
            with st.expander("Polynomial f(x) mod p", expanded=True):
                st.latex(f"f(x) \equiv {poly_mod} \pmod{{{p}}}")

    with col2:
        with st.expander(f"📊 Fp Plot (p={p})", expanded=True):
            fig, ax = plt.subplots()
            ax.scatter(x_coords, y_coords, facecolors='none', edgecolors='#e74c3c', s=100)
            ax.set_xlim(-0.5, p-0.5); ax.set_ylim(-0.5, p-0.5)
            ax.set_xticks(range(p)); ax.set_yticks(range(p))
            ax.grid(True, alpha=0.2)
            st.pyplot(fig)
