import streamlit as st
from sympy import symbols, simplify, Mod, Inverse, expand
import matplotlib.pyplot as plt

def lagrange_fp():
    points_list = []
    x_coords = []
    y_coords = []
    
    # Divide the page into four equal columns
    col1, col2 = st.columns([8, 5])

    with col1:
        p = st.number_input("Enter prime number (p):", min_value=2, value=7)
        num_points = st.number_input("Number of points:", min_value=2, max_value=20, value=3, step=1)
        for i in range(num_points):
            x = st.number_input(f"X{i+1}:", format="%d")
            y = st.number_input(f"Y{i+1}:", format="%d")
            points_list.append((int(x) % p ,int(y) % p))
            x_coords.append(int(x) % p)
            y_coords.append(int(y) % p)
            
        with st.expander(f"📍 Points ({len(points_list)} points):", expanded=False):
            # Removed the gray background div and used direct styled text
            points_html = f"""
                <div style='
                    font-family: monospace;
                    font-size: 16px; 
                    line-height: 1.6;
                    color: #2c3e50;
                    padding: 5px 0px;
                    word-break: break-all;'>
                    {{ {points_list} }}
                </div>
            """
        st.markdown(points_html, unsafe_allow_html=True)
        # Divider after the expander
        st.divider()
        poly_mod = lagrange_mod_p(x_coords, y_coords, p)
        # 1. Create expander with clear title
        with st.expander("The f(x) polynomial", expanded=True): # Already True
            # 4 columns: three for inputs, one for the formula
            st.latex(f"f(x)={poly_mod}\\pmod{{{p}}}")
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with col2:                 
        
        # Visual plot rendering inside an expander: Using expanded=True to keep the plot visible by default
        with st.expander(f"📊 Visualization over Fp (p={p}):", expanded=True):
            fig, ax = plt.subplots(figsize=(6, 6))
            
            # Scatter plot styling
            ax.scatter(x_coords, y_coords, s=20, facecolors='none', edgecolors='#3498db', linewidth=1.0)
            
            ax.set_xlim(-0.5, p - 0.5)
            ax.set_ylim(-0.5, p - 0.5)
            ax.grid(True, linestyle='-', alpha=0.3)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_xticks(range(0, p, max(1, p // 10)))
            ax.set_yticks(range(0, p, max(1, p // 10)))
            
            # Display the plot inside the expander
            st.pyplot(fig)

def lagrange():
    points_list = []
    x_coords = []
    y_coords = []
    
    # Divide the page into four equal columns
    col1, col2 = st.columns([8, 5])

    with col1:
        # Input fields for x and y values
        num_points = st.number_input("Number of points:", min_value=1, value=3)
        x_max = 1;
        y_max = 1;
        for i in range(num_points):
            x = st.number_input(f"X{i+1}:", format="%f")
            y = st.number_input(f"Y{i+1}:", format="%f")
            points_list.append((x,y))
            x_coords.append(x)
            y_coords.append(y)
            x_max = max(x_max, abs(x));
            y_max = max(y_max, abs(y));
        axis_max = int(max(x_max, y_max))+1
        with st.expander(f"📍 Points ({len(x_coords)} points):", expanded=False):
            # Removed the gray background div and used direct styled text
            points_html = f"""
                <div style='
                    font-family: monospace;
                    font-size: 16px; 
                    line-height: 1.6;
                    color: #2c3e50;
                    padding: 5px 0px;
                    word-break: break-all;'>
                    {{ {points_list} }}
                </div>
            """
        st.markdown(points_html, unsafe_allow_html=True)
        # Divider after the expander
        st.divider()
        poly = lagrange_real(x_coords, y_coords)
        # 1. Create expander with clear title
        with st.expander("The f(x) polynomial", expanded=True): # Already True
            # 4 columns: three for inputs, one for the formula
            st.latex(f"f(x)={poly}")
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with col2:                 
        
        # Visual plot rendering inside an expander: Using expanded=True to keep the plot visible by default
        with st.expander(f"📊 Visualization over real numbers:", expanded=True):
            fig, ax = plt.subplots(figsize=(6, 6))
            
            # Scatter plot styling
            ax.scatter(x_coords, y_coords, s=20, facecolors='none', edgecolors='#3498db', linewidth=1.0)
            
            ax.set_xlim(-0.5, axis_max)
            ax.set_ylim(-0.5, axis_max)
            ax.grid(True, linestyle='-', alpha=0.3)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_xticks(range(-axis_max, axis_max, max(1, axis_max // 10)))
            ax.set_yticks(range(-axis_max, axis_max, max(1, axis_max // 10)))
            
            # Display the plot inside the expander
            st.pyplot(fig)
            
    # Real part
def lagrange_real(x_coords, y_coords):
    len_ys = len(y_coords)
    res = 0
    for i in range(len_ys):
        res += lagrange_basis(x_coords, i)*y_coords[i]
    return res

def lagrange_basis(x_coordinates, j):
    """
    Compute the j-th Lagrange basis polynomial.

    Args:
        x: The variable.
        H: The x-coordinates of the data points.
        j: The index of the basis polynomial.

    Returns:
        The value of the j-th Lagrange basis polynomial at x.
    """
    x = symbols('x')
    basis = 1
    for m in range(len(x_coordinates)):
        if m != j:
            basis *= (x - x_coordinates[m]) / (x_coordinates[j] - x_coordinates[m])
    return basis

def Lagrange_polys(x_coordinates):
    polys = list([]);
    for i in range(len(x_coordinates)):
        polys.append(lagrange_basis(x_coordinates,i));
    return polys;
# Finite Fields
def lagrange_mod_p(x_coords, y_coords, p):
    len_ys = len(y_coords)
    res = 0
    for i in range(len_ys):
        res += lagrange_basis_modp(x_coords, i, p)*y_coords[i]
    return res
def lagrange_basis_modp(x_coordinates, j, p):
    """
    Compute the j-th Lagrange basis polynomial.

    Args:
        x: The variable.
        x_coordinates: The x-coordinates of the data points.
        j: The index of the basis polynomial.

    Returns:
        The value of the j-th Lagrange basis polynomial at x.
    """
    x = symbols('x')
    basis = 1
    for m in range(len(x_coordinates)):
        if m != j:
            den = pow((x_coordinates[j] - x_coordinates[m]), -1, p)
            basis *= ((x - x_coordinates[m])* den)
    return basis

def Lagrange_polys_modp(x_coordinates, p):
    polys = list([]);
    for i in range(len(x_coordinates)):
        polys.append(lagrange_basis_modp(x_coordinates,i, p));
    return polys;
