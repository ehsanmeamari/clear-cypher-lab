import streamlit as st
from sympy import symbols, simplify, expand, lambdify, latex
import matplotlib.pyplot as plt
import numpy as np

def lagrange_basis_real(x_coordinates, j):
    x = symbols('x')
    basis = 1
    for m in range(len(x_coordinates)):
        if m != j:
            basis *= (x - x_coordinates[m]) / (x_coordinates[j] - x_coordinates[m])
    return simplify(basis)

def lagrange_real_calc(x_coords, y_coords):
    res = 0
    for i in range(len(y_coords)):
        res += lagrange_basis_real(x_coords, i) * y_coords[i]
    return expand(res)

def lagrange_basis_modp(x_coordinates, j, p):
    x = symbols('x')
    basis = 1
    for m in range(len(x_coordinates)):
        if m != j:
            denominator = int(x_coordinates[j] - x_coordinates[m])
            den_inv = pow(denominator, -1, p)
            basis *= (x - x_coordinates[m]) * den_inv
    return basis

def lagrange_mod_p_calc(x_coords, y_coords, p):
    res = 0
    for i in range(len(y_coords)):
        res += lagrange_basis_modp(x_coords, i, p) * y_coords[i]
    return simplify(res % p)

def lagrange_real_ui():
    x_coords, y_coords = [], []
    col1, col2 = st.columns([7, 5])
    with col1:
        num_points = st.number_input("Number of points:", min_value=2, value=3, key="re_num")
        for i in range(0, num_points, 3):
            cols = st.columns(min(3, num_points - i) * 2)
            for j in range(min(3, num_points - i)):
                with cols[j*2]: x = st.number_input(f"X{i+j+1}:", value=float(i+j), key=f"rx{i+j}")
                with cols[j*2+1]: y = st.number_input(f"Y{i+j+1}:", value=float((i+j)**2), key=f"ry{i+j}")
                x_coords.append(x)
                y_coords.append(y)

        if len(set(x_coords)) != len(x_coords):
            st.error("Error: X coordinates must be distinct.")
        else:
            poly = lagrange_real_calc(x_coords, y_coords)
            with st.expander("Resulting Polynomial f(x)", expanded=True):
                st.latex(f"f(x) = {latex(poly)}")

    with col2:
        with st.expander("📊 Visualization", expanded=True):
            if len(set(x_coords)) == len(x_coords):
                x_sym = symbols('x')
                poly = lagrange_real_calc(x_coords, y_coords)
                f = lambdify(x_sym, poly, 'numpy')
                x_min = min(x_coords) - 1
                x_max = max(x_coords) + 1
                x_plot = np.linspace(x_min, x_max, 500)
                y_plot = f(x_plot)
                fig, ax = plt.subplots()
                ax.plot(x_plot, y_plot, color='#2ecc71', linewidth=2)
                ax.scatter(x_coords, y_coords, color='#3498db', zorder=5, s=60)
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)

def lagrange_fp_ui():
    x_coords, y_coords = [], []
    col1, col2 = st.columns([7, 5])
    with col1:
        p = st.number_input("Prime number (p):", min_value=2, value=7, key="fp_p")
        num_points = st.number_input("Number of points:", min_value=2, value=3, key="fp_num")
        for i in range(0, num_points, 3):
            cols = st.columns(min(3, num_points - i) * 2)
            for j in range(min(3, num_points - i)):
                with cols[j*2]: x = st.number_input(f"X{i+j+1}:", value=i+j, key=f"fpx{i+j}") % p
                with cols[j*2+1]: y = st.number_input(f"Y{i+j+1}:", value=(i+j+1) % p, key=f"fpy{i+j}") % p
                x_coords.append(x)
                y_coords.append(y)

        if len(set(x_coords)) != len(x_coords):
            st.error("Error: X coordinates must be unique in $\mathbb{F}_p$.")
        else:
            poly_mod = lagrange_mod_p_calc(x_coords, y_coords, p)
            with st.expander("Polynomial f(x) mod p", expanded=True):
                st.latex(f"f(x) \\equiv {latex(poly_mod)} \\pmod{{{p}}}")

    with col2:
        with st.expander(f"📊 Fp Plot (p={p})", expanded=True):
            fig, ax = plt.subplots()
            ax.scatter(x_coords, y_coords, facecolors='none', edgecolors='#e74c3c', s=100)
            ax.set_xlim(-0.5, p - 0.5)
            ax.set_ylim(-0.5, p - 0.5)
            ax.set_xticks(range(p))
            ax.set_yticks(range(p))
            ax.grid(True, alpha=0.2)
            st.pyplot(fig)
