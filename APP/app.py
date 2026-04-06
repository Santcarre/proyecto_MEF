import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.title("2D Heat Conduction - Laplace Solution")
st.subheader("Daniel Santiago Carreño Briceño")
st.subheader("Finite Element Methods")

# -----------------------------
# Parameters
# -----------------------------
L = st.slider("Plate Length L", 1.0, 5.0, 2.0)
W = st.slider("Plate Height W", 1.0, 5.0, 1.0)
N_terms = st.slider("Number of Fourier Modes", 1, 50, 5)

nx, ny = 100, 100
x = np.linspace(0, L, nx)
y = np.linspace(0, W, ny)

X, Y = np.meshgrid(x, y)

# -----------------------------
# Analytical Solution
# -----------------------------
T = np.zeros_like(X)

for n in range(1, N_terms + 1):

    if n % 2 == 0:
        continue

    coef = (
        4
        / (n * np.pi * np.sinh(n * np.pi * W / L))
    )

    T += (
        coef
        * np.sin(n * np.pi * X / L)
        * np.sinh(n * np.pi * Y / L)
    )

# -----------------------------
# 2D Heatmap
# -----------------------------
st.subheader("Temperature Field (2D)")

fig, ax = plt.subplots()

c = ax.contourf(X, Y, T, 50)
fig.colorbar(c)

ax.set_xlabel("x")
ax.set_ylabel("y")

st.pyplot(fig)

# -----------------------------
# 3D Surface
# -----------------------------
st.subheader("Temperature Surface (3D)")

fig3d = plt.figure()
ax3d = fig3d.add_subplot(111, projection="3d")

ax3d.plot_surface(X, Y, T)

ax3d.set_xlabel("x")
ax3d.set_ylabel("y")
ax3d.set_zlabel("Temperature")

st.pyplot(fig3d)