import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
def load_data():
    df = pd.read_csv("dataset/covid_19_indonesia_time_series_all.csv")
    return df

# Filter data berdasarkan tahun
def filter_data(df, year=None):
    if year:
        df = df[df['Date'].astype(str).str.contains(str(year))]
    return df

# Sidebar pilih tahun
def select_year():
    return st.sidebar.selectbox(
        "Pilih Tahun 📅",
        options=[None, 2020, 2021, 2022],
        format_func=lambda x: "Semua Tahun" if x is None else str(x)
    )

# Menampilkan data
def show_data(df):

    selected_columns = ['Location'] + list(
        df.loc[:, 'New Cases':'Total Recovered'].columns
    )

    df_selected = df[selected_columns]

    st.subheader("Data Covid-19 Indonesia 🔴⚪")

    st.dataframe(df_selected.head(10), width='stretch')

    # Menampilkan total kasus keseluruhan
    total_kasus = df["Total Cases"].sum()

    st.subheader("Total Kasus Keseluruhan")
    st.write(total_kasus)

    # Tombol hapus sesi
    if st.button("Hapus Data Sesi"):
        st.session_state.clear()
        st.rerun()

    # Statistik deskriptif
    st.subheader("Statistik Deskriptif Dataset")
    st.write(df_selected.describe())

# Fungsi total kasus
def total_case(df):
    total_kasus = df['New Cases'].sum()
    return total_kasus

# Fungsi total kematian
def total_death(df):
    total_mati = df['New Deaths'].sum()
    return total_mati

# Fungsi total sembuh
def total_recovery(df):
    total_sembuh = df['New Recovered'].sum()
    return total_sembuh

# Scoreboard metric
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

# Pie chart
def pie_chart1(df):

    total_mati = total_death(df)
    total_sembuh = total_recovery(df)

    # Data chart
    data = {
        'Status': ['Meninggal', 'Sembuh'],
        'Jumlah': [total_mati, total_sembuh]
    }

    # Pie chart
    fig = px.pie(
        data,
        names='Status',
        values='Jumlah',
        title='Perbandingan Total Kematian vs Total Kesembuhan',
        hole=0.5,
        color_discrete_sequence=['#ff6459', '#4de89f']
    )

    st.plotly_chart(fig, width='stretch')