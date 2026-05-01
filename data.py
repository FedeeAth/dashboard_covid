import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# LOAD DATA
# =========================
def load_data():

    df = pd.read_csv(
        "dataset/covid_19_indonesia_time_series_all.csv"
    )

    # Hapus outlier Indonesia
    df = df[df["Location"] != "Indonesia"]

    return df


# =========================
# FILTER DATA
# =========================
def filter_data(df, year=None, locations=None):

    # Filter tahun
    if year:
        df = df[df['Date'].astype(str).str.contains(str(year))]

    # Filter multi lokasi
    if locations:
        df = df[df['Location'].isin(locations)]

    return df


# =========================
# SELECT YEAR
# =========================
def select_year():

    return st.sidebar.selectbox(
        "Pilih Tahun 📅",
        options=[None, 2020, 2021, 2022],
        format_func=lambda x:
        "Semua Tahun" if x is None else str(x)
    )


# =========================
# SELECT LOCATION
# =========================
def select_location(df):

    locations = sorted(df['Location'].unique())

    return st.sidebar.multiselect(
        "Pilih Provinsi 🗺️",
        options=locations
    )


# =========================
# SHOW DATA
# =========================
def show_data(df):

    selected_columns = ['Location'] + list(
        df.loc[:, 'New Cases':'Total Recovered'].columns
    )

    df_selected = df[selected_columns]

    st.subheader("Data Covid-19 Indonesia 🔴⚪")

    st.dataframe(
        df_selected.head(10),
        width='stretch'
    )

    # Total kasus
    total_kasus = total_case(df)

    st.subheader("Total Kasus Keseluruhan")
    st.write(total_kasus)

    # Tombol reset
    if st.button("Hapus Data Sesi"):
        st.session_state.clear()
        st.rerun()

    # Statistik
    st.subheader("Statistik Deskriptif Dataset")
    st.write(df_selected.describe())


# =========================
# TOTAL CASE
# =========================
def total_case(df):

    total_kasus = (
        df.sort_values('Date')
        .groupby('Location', as_index=False)
        .last()
    )

    return total_kasus['Total Cases'].sum()


# =========================
# TOTAL DEATH
# =========================
def total_death(df):

    total_mati = (
        df.sort_values('Date')
        .groupby('Location', as_index=False)
        .last()
    )

    return total_mati['Total Deaths'].sum()


# =========================
# TOTAL RECOVERY
# =========================
def total_recovery(df):

    total_sembuh = (
        df.sort_values('Date')
        .groupby('Location', as_index=False)
        .last()
    )

    return total_sembuh['Total Recovered'].sum()


# =========================
# SCOREBOARD
# =========================
def kolom(df):

    kasus = total_case(df)
    kematian = total_death(df)
    sembuh = total_recovery(df)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        label="📈 Total Kasus",
        value=kasus,
        border=True
    )

    col2.metric(
        label="💀 Total Kematian",
        value=kematian,
        border=True
    )

    col3.metric(
        label="💚 Total Sembuh",
        value=sembuh,
        border=True
    )


# =========================
# PIE CHART
# =========================
def pie_chart1(df):

    total_mati = total_death(df)
    total_sembuh = total_recovery(df)

    data = {
        'Status': ['Meninggal', 'Sembuh'],
        'Jumlah': [total_mati, total_sembuh]
    }

    fig = px.pie(
        data,
        names='Status',
        values='Jumlah',
        title='Perbandingan Total Kematian vs Total Kesembuhan',
        hole=0.5,
        color_discrete_sequence=['#ff6459', '#4de89f']
    )

    st.plotly_chart(fig, width='stretch')


# =========================
# BAR CHART DEATH
# =========================
def bar_chart1(df):

    df_last = (
        df.sort_values('Date')
        .groupby('Location', as_index=False)
        .last()
    )

    top5 = df_last.nlargest(5, 'Total Deaths')

    fig = px.bar(
        top5,
        x='Location',
        y='Total Deaths',
        color='Total Deaths',
        color_continuous_scale='Reds',
        title='5 Provinsi dengan Kematian Tertinggi'
    )

    fig.update_layout(
        xaxis_title='Provinsi',
        yaxis_title='Total Kematian',
        title_x=0.5
    )

    st.plotly_chart(fig, width='stretch')


# =========================
# BAR CHART RECOVERY
# =========================
def bar_chart2(df):

    df_last = (
        df.sort_values('Date')
        .groupby('Location', as_index=False)
        .last()
    )

    top5 = df_last.nlargest(5, 'Total Recovered')

    fig = px.bar(
        top5,
        x='Location',
        y='Total Recovered',
        color='Total Recovered',
        color_continuous_scale='Greens',
        title='5 Provinsi dengan Kesembuhan Tertinggi'
    )

    fig.update_layout(
        xaxis_title='Provinsi',
        yaxis_title='Total Kesembuhan',
        title_x=0.5
    )

    st.plotly_chart(fig, width='stretch')


# =========================
# MAP CHART
# =========================
def map_chart(df, year=None):

    df['Date'] = pd.to_datetime(df['Date'])

    # Filter tahun
    if year:
        df = df[df['Date'].dt.year == year]

    # Agregasi data
    df_agg = df.groupby(
        ['Location', 'Latitude', 'Longitude'],
        as_index=False
    )['New Cases'].sum()

    df_map = df_agg.dropna(
        subset=['Latitude', 'Longitude', 'New Cases']
    )

    # Validasi data
    if df_map.empty:
        st.info("Tidak ada data untuk ditampilkan di peta.")
        return

    # Map chart
    fig = px.scatter_mapbox(
        df_map,
        lat="Latitude",
        lon="Longitude",
        size="New Cases",
        color="New Cases",
        hover_name="Location",
        zoom=3,
        center={"lat": -2.5, "lon": 118},
        size_max=20,
        opacity=0.7,
        color_continuous_scale="OrRd",
        title=f"Sebaran Kasus Baru Covid-19 di Indonesia"
    )

    # Style map
    fig.update_layout(
        mapbox_style="carto-positron",
        height=600,
        margin={"r":0,"t":50,"l":0,"b":0}
    )

    st.plotly_chart(fig, width='stretch')