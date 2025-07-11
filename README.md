# Sistem Uang Kas Mahasiswa

Aplikasi pencatatan uang kas mahasiswa berbasis Python yang menyediakan fitur manajemen data mahasiswa, pembayaran uang kas, tunggakan global, serta riwayat pembayaran. Aplikasi ini dilengkapi dengan antarmuka GUI menggunakan Tkinter, login admin, dan penyimpanan data permanen berbasis file CSV.

## Fitur Utama

- Login Admin
- Tambah dan Hapus Mahasiswa
- Pembayaran Kas Mahasiswa
- Fitur Undo Pembayaran (menggunakan struktur data Stack)
- Tambah Tunggakan Global
- Tampilkan Tabel Data Mahasiswa
- Tampilkan Riwayat Pembayaran
- Hitung Total Uang Kas
- Refresh Data
- Penyimpanan Data ke File CSV
- Log Aktivitas Admin (File log.csv)

## Struktur Data yang Digunakan

- **HashMap (Dictionary)**  
  Untuk menyimpan data mahasiswa beserta riwayat pembayaran mereka.

- **Stack (Undo Pembayaran)**  
  Untuk membatalkan pembayaran terakhir yang dilakukan.

## Struktur Folder
- uang-kas-mahasiswa/
- ├── main.py
- ├── auth.py
- ├── database.py
- ├── logic.py
- ├── utils.py
- ├── data/
- │ ├── data_mahasiswa.csv
- │ ├── kas_mahasiswa.csv
- │ ├── log.csv
- │ └── admin.csv
- └── README.md


# Python Library yang digunakan:
- tkinter — untuk GUI
- csv — untuk membaca/menulis file CSV
- datetime — untuk mencatat waktu transaksi
- os — untuk pengecekan file/folder

Jika menjalankan program dan mendapatkan error seperti ModuleNotFoundError: No module named 'tkinter', maka Anda harus menginstal Tkinter terlebih dahulu (tergantung sistem operasi).

Windows:
- *pip install tk*

Linux (Debian/Ubuntu):
- *sudo apt-get install python3-tk*
