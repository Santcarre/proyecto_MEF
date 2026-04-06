import html as html_module
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 — registra proyección 3D


def show_pdf(relative_path: str, height: int = 800) -> None:
    """Muestra el PDF con `st.pdf` y un enlace para abrirlo en otra pestaña.

    No usamos un `<iframe>` propio con la URL estática: Chrome suele bloquear PDFs
    dentro de iframes anidados (p. ej. dentro del componente HTML de Streamlit).
    El enlace directo a `app/static/...` no tiene ese problema.
    """
    base = pathlib.Path(__file__).resolve().parent
    pdf_path = base / relative_path
    if not pdf_path.is_file():
        st.error(f"No se encontró el PDF: `{pdf_path}`")
        st.caption(
            "Compila el .tex y guarda el PDF en `APP/static/`, o copia aquí los archivos esperados."
        )
        return

    fname = pdf_path.name
    url = f"app/static/{fname}"

    c1, c2 = st.columns([1, 2])
    with c1:
        # st.link_button(..., open_in_new_tab=) no está en todas las versiones de Streamlit.
        safe_href = html_module.escape(url)
        st.markdown(
            f'<a href="{safe_href}" target="_Blank" rel="noopener noreferrer" '
            'style="display:inline-block;padding:0.45rem 0.9rem;background:black;color:white;'
            'border-radius:0.5rem;text-decoration:none;font-weight:600;">Open</a>',
            unsafe_allow_html=True,
        )
    with c2:
        st.caption(
            "Press the button to open the PDF in a new tab and view it in full screen."
        )

    st.pdf(str(pdf_path), height=height)


tab1, tab2, tab3 = st.tabs(
    ["Simulation", "Slides", "Handwritten Notes"]
)

with tab1:
    st.write("Interactive heat conduction solution")
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

with tab2:
    show_pdf("static/Expo_3.pdf")

with tab3:
    show_pdf("static/Expo_3_MEF.pdf")
