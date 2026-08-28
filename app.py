import streamlit as st
import pandas as pd
import sqlite3

# Konfigurasi Halaman & Dark Mode Default
st.set_page_config(
    page_title="RD Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi Database SQLite
def init_db():
    conn = sqlite3.connect("database.db", check_same_thread=False)
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

def get_data():
    conn = sqlite3.connect("database.db")
    df = pd.read_sql("SELECT * FROM channels", conn)
    conn.close()
    return df

# Navigasi Sidebar Sederhana
st.sidebar.title("🎬 RD Studio")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Pilih Menu:", ["📊 Overview Dashboard", "🎬 Video Analytics", "📈 Growth Analytics", "🔥 Top-Performing Videos"])

# Menu Overview Dashboard
if menu == "📊 Overview Dashboard":
    st.title("📊 Overview Dashboard")
    st.markdown("Kelola data channel YouTube Anda dengan mudah di sini.")
    
    # Tombol untuk memunculkan Form Tambah Channel
    with st.expander("➕ Tambah Channel Baru ke Database"):
        with st.form("add_form_main", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                nama = st.text_input("Nama Channel")
                inisial = st.text_input("Inisial")
            with col2:
                url = st.text_input("URL Channel")
                pic = st.text_input("PIC")
            with col3:
                email = st.text_input("Email Owner")
                jadwal = st.text_input("Status Jadwal", value="30 hari lagi")
            
            lulus = st.selectbox("Status Lulus", ["Belum", "Sudah"])
            submitted = st.form_submit_button("Simpan Channel Baru")
            
            if submitted:
                if nama:
                    conn = sqlite3.connect("database.db")
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO channels (nama_channel, inisial, url_channel, pic, email_owner, status_jadwal, status_lulus) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                   (nama, inisial, url, pic, email, jadwal, lulus))
                    conn.commit()
                    conn.close()
                    st.success("Channel berhasil ditambahkan! Silakan refresh halaman.")
                else:
                    st.error("Nama channel wajib diisi.")

    df = get_data()
    
    # Masukkan data demo jika database masih kosong
    if df.empty:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO channels (nama_channel, inisial, url_channel, pic, email_owner, status_jadwal, status_lulus) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                       ("Manantial de Esp...", "MDE", "https://youtube.com/...", "Ardhi", "archimoonlord@gmail.com", "33 hari lagi", "Sudah"))
        cursor.execute("INSERT INTO channels (nama_channel, inisial, url_channel, pic, email_owner, status_jadwal, status_lulus) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                       ("El Cuervo Errante", "ECE", "https://youtube.com/...", "Ardhi", "gundamjogjareborn@gmail.com", "39 hari lagi", "Belum"))
        conn.commit()
        conn.close()
        df = get_data()

    # Fitur Pencarian
    search = st.text_input("🔎 Cari nama channel, URL, atau email...")
    if search:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]

    st.markdown("### Daftar Channel & Aksi Edit")
    st.markdown("Klik pada salah satu baris channel di bawah untuk memperbarui atau menghapus data.")

    # Menampilkan daftar dengan opsi Edit/Hapus per baris yang interaktif
    for index, row in df.iterrows():
        with st.expander(f"Channel: {row['nama_channel']} | PIC: {row['pic']} | Status: {row['status_lulus']}"):
            with st.form(f"edit_form_{row['id']}"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    e_nama = st.text_input("Nama Channel", value=row['nama_channel'])
                    e_inisial = st.text_input("Inisial", value=row['inisial'])
                with c2:
                    e_url = st.text_input("URL Channel", value=row['url_channel'])
                    e_pic = st.text_input("PIC", value=row['pic'])
                with c3:
                    e_email = st.text_input("Email Owner", value=row['email_owner'])
                    e_jadwal = st.text_input("Status Jadwal", value=row['status_jadwal'])
                
                e_lulus = st.selectbox("Status Lulus", ["Belum", "Sudah"], index=0 if row['status_lulus']=="Belum" else 1)
                
                b1, b2 = st.columns(2)
                with b1:
                    update_btn = st.form_submit_button("💾 Update Perubahan")
                with b2:
                    delete_btn = st.form_submit_button("🗑️ Hapus Channel Ini")
                
                if update_btn:
                    conn = sqlite3.connect("database.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE channels SET nama_channel=?, inisial=?, url_channel=?, pic=?, email_owner=?, status_jadwal=?, status_lulus=?
                        WHERE id=?
                    """, (e_nama, e_inisial, e_url, e_pic, e_email, e_jadwal, e_lulus, row['id']))
                    conn.commit()
                    conn.close()
                    st.success("Data berhasil diperbarui!")
                
                if delete_btn:
                    conn = sqlite3.connect("database.db")
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM channels WHERE id=?", (row['id'],))
                    conn.commit()
                    conn.close()
                    st.success("Channel berhasil dihapus!")

elif menu == "🎬 Video Analytics":
    st.title("🎬 Video Analytics")
    st.write("Fitur analitik performa video per channel.")

elif menu == "📈 Growth Analytics":
    st.title("📈 Growth Analytics")
    st.write("Grafik pertumbuhan subscriber dan views.")

elif menu == "🔥 Top-Performing Videos":
    st.title("🔥 Top-Performing Videos")
    st.write("Daftar video dengan performa terbaik.")