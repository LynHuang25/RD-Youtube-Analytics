import streamlit as st
import pandas as pd
import sqlite3

# Konfigurasi Halaman & Dark Mode Default
st.set_page_config(
    page_title="Production Elkira Studio (PES)",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi Database SQLite Sederhana
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_channel TEXT,
            inisial TEXT,
            url_channel TEXT,
            pic TEXT,
            email_owner TEXT,
            status_jadwal TEXT,
            status_lulus TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Navigasi Menu / Sidebar
st.sidebar.title("🎬 Production Elkira Studio")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Pilih Menu:", ["📊 Overview Dashboard", "🎬 Video Analytics", "📈 Growth Analytics", "🔥 Top-Performing Videos"])

# Konten berdasarkan Menu
if menu == "📊 Overview Dashboard":
    st.title("📊 Overview Dashboard")
    st.markdown("Kelola data channel YouTube Anda dengan mudah di sini.")
    
    # Contoh Tabel dengan Data Demo / SQLite
    conn = sqlite3.connect("database.db")
    df = pd.read_sql("SELECT * FROM channels", conn)
    conn.close()
    
    if df.empty:
        st.info("Belum ada data channel. Menggunakan data demo...")
        df = pd.DataFrame([
            {"nama_channel": "Manantial de Esp...", "inisial": "MDE", "url_channel": "https://youtube.com/...", "pic": "Ardhi", "email_owner": "archimoonlord@gmail.com", "status_jadwal": "33 hari lagi", "status_lulus": "Sudah"},
            {"nama_channel": "El Cuervo Errante", "inisial": "ECE", "url_channel": "https://youtube.com/...", "pic": "Ardhi", "email_owner": "gundamjogjareborn@gmail.com", "status_jadwal": "39 hari lagi", "status_lulus": "Belum"}
        ])
    
    # Fitur Search & Sorting
    search_query = st.text_input("🔎 Cari nama channel, URL, atau email...")
    if search_query:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
        
    st.dataframe(df, use_container_width=True)

elif menu == "🎬 Video Analytics":
    st.title("🎬 Video Analytics")
    st.write("Fitur analitik performa video per channel akan ditampilkan di sini.")

elif menu == "📈 Growth Analytics":
    st.title("📈 Growth Analytics")
    st.write("Grafik pertumbuhan subscriber dan views.")

elif menu == "🔥 Top-Performing Videos":
    st.title("🔥 Top-Performing Videos")
    st.write("Daftar video dengan performa terbaik.")