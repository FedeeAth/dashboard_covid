import streamlit as st
import pandas as pd

# LOAD DATA
def load_data():
    df = pd.read_csv("dataset/covid_19_indonesia_time_series_all.csv")
    return df

# TOTAL KASUS KESELURUHAN
def total_kasus():
    df = load_data()
    
    st.subheader("📑 Total Kasus Keseluruhan")
    
    total_cases = df["Total Cases"].sum()
    st.write("Total Kasus Keseluruhan:", int(total_cases))

# TAMPIL DATA (KOLOM TERTENTU SAJA)
def tampil_data():
    df = load_data()
    
    st.subheader("🦠 Data COVID-19 Indonesia")
    
    # Menampilkan hanya kolom Location sampai Total Recovered
    df_filtered = df.loc[:, "Location":"Total Recovered"]
    
    st.dataframe(df_filtered.head(10))

# STATISTIK DESKRIPTIF
def statistik_data():
    df = load_data()
    
    st.subheader("📊 Statistik Deskriptif Dataset")
    
    df_filtered = df.loc[:, "Location":"Total Recovered"]
    st.write(df_filtered.describe())


# COPYRIGHT
def copyright_footer():
    st.markdown("---")
    st.markdown(
        "© 2026 Farrel Vega Athallah | NPM: 184240005"
    )