import streamlit as st
from data import tampil_data, statistik_data, total_kasus, copyright_footer

def judul():
    st.title("📊 Dashboard COVID-19")
    st.write(
        "Selamat datang di dashboard interaktif untuk menganalisis data COVID-19. "
        "Anda dapat melihat data terbaru mengenai kasus COVID-19."
    )

# Sidebar
st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Halaman", ["Home", "Halaman Data"])

# Routing halaman
if menu == "Home":
    judul()
    copyright_footer()

elif menu == "Halaman Data":
    judul()
    total_kasus()
    tampil_data()
    statistik_data()
    copyright_footer()