import streamlit as st
from data import *

# =========================
# JUDUL
# =========================
def judul():

    st.title("🔴 Dashboard Covid-19 Indonesia")

    st.markdown(
        """
        Selamat datang di dashboard interaktif
        untuk menganalisis data Covid-19
        di Indonesia 🔴⚪
        """
    )


# =========================
# SIDEBAR
# =========================
st.sidebar.title("🏙️ Navigasi")

menu = st.sidebar.radio(
    "Pilih Halaman",
    ["Home", "Halaman Data"]
)


# =========================
# HOME
# =========================
if menu == "Home":

    judul()

    # Load data
    df = load_data()

    # Filter
    year = select_year()

    locations = select_location(df)

    # Filter dataframe
    df_filtered = filter_data(
        df,
        year,
        locations
    )

    # Metric
    kolom(df_filtered)

    # Pie chart
    pie_chart1(df_filtered)

    # Bar chart
    bar_chart1(df_filtered)

    # Bar chart
    bar_chart2(df_filtered)

    # Map chart
    map_chart(df_filtered, year)


# =========================
# HALAMAN DATA
# =========================
elif menu == "Halaman Data":

    judul()

    # Load data
    df = load_data()

    # Filter
    year = select_year()

    locations = select_location(df)

    # Filter dataframe
    df_filtered = filter_data(
        df,
        year,
        locations
    )

    # Show data
    show_data(df_filtered)
    
    # Show data
show_data(df_filtered)

# =========================
# FOOTER
# =========================
st.markdown("---")

st.markdown(
    """
    <div style='text-align: center; padding: 10px;'>
        <h4>📊 Dashboard Covid-19 Indonesia</h4>
        <p>
            Dibuat oleh <b>Farrel Vega Athallah</b><br>
            NPM: <b>184240005</b>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)