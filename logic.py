import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import os, csv

from database import mahasiswa, simpan_mahasiswa, simpan_pembayaran, load_mahasiswa, load_tunggakan
from utils import tulis_log, total_bayar, sisa_tunggakan, total_tagihan

FILE_KAS = "data/kas_mahasiswa.csv"
undo_stack = []

def tambah_mahasiswa(user):
    win = tk.Toplevel()
    win.title("Tambah Mahasiswa")

    nim = tk.Entry(win)
    nama = tk.Entry(win)
    kelas = tk.Entry(win)

    for i, label in enumerate(["NIM", "Nama", "Kelas"]):
        tk.Label(win, text=label).grid(row=i, column=0)
    for i, entry in enumerate([nim, nama, kelas]):
        entry.grid(row=i, column=1)

    def simpan():
        n = nim.get()
        if n in mahasiswa:
            messagebox.showerror("Gagal", "NIM sudah ada.")
            return
        mahasiswa[n] = {'nama': nama.get(), 'kelas': kelas.get(), 'riwayat': []}
        simpan_mahasiswa()
        tulis_log(user, f"Tambah mahasiswa: {n} - {nama.get()}")
        messagebox.showinfo("Sukses", "Mahasiswa ditambahkan.")
        win.destroy()

    tk.Button(win, text="Simpan", command=simpan).grid(row=3, column=0, columnspan=2)

def hapus_mahasiswa(user):
    win = tk.Toplevel()
    win.title("Hapus Mahasiswa")

    tk.Label(win, text="NIM:").pack()
    nim = tk.Entry(win)
    nim.pack()

    def hapus():
        n = nim.get()
        if n not in mahasiswa:
            messagebox.showerror("Error", "Tidak ditemukan.")
            return
        nama = mahasiswa[n]['nama']
        del mahasiswa[n]
        simpan_mahasiswa()

        if os.path.exists(FILE_KAS):
            rows = []
            with open(FILE_KAS, newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['NIM'] != n:
                        rows.append(row)
            with open(FILE_KAS, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['NIM', 'Nama', 'Kelas', 'Jumlah', 'Tanggal'])
                writer.writeheader()
                writer.writerows(rows)

        tulis_log(user, f"Hapus mahasiswa: {n} - {nama}")
        messagebox.showinfo("Berhasil", f"{n} dihapus.")
        win.destroy()

    tk.Button(win, text="Hapus", command=hapus).pack(pady=5)

def bayar_kas(user):
    win = tk.Toplevel()
    win.title("Bayar Kas")

    nim = tk.Entry(win)
    jumlah = tk.Entry(win)

    tk.Label(win, text="NIM").grid(row=0, column=0)
    tk.Label(win, text="Nominal").grid(row=1, column=0)
    nim.grid(row=0, column=1)
    jumlah.grid(row=1, column=1)

    def bayar():
        n = nim.get()
        if n not in mahasiswa:
            messagebox.showerror("Gagal", "Tidak ditemukan.")
            return
        try:
            jml = int(jumlah.get())
        except:
            messagebox.showerror("Gagal", "Nominal salah.")
            return
        mahasiswa[n]['riwayat'].append({'jumlah': jml, 'tanggal': datetime.now().strftime('%Y-%m-%d')})
        undo_stack.append({'nim': n, 'jumlah': jml, 'tanggal': datetime.now().strftime('%Y-%m-%d')})
        simpan_pembayaran(n, jml)
        simpan_mahasiswa()
        tulis_log(user, f"Pembayaran Rp{jml} oleh {n}")
        messagebox.showinfo("Sukses", "Pembayaran dicatat.")
        win.destroy()

    tk.Button(win, text="Bayar", command=bayar).grid(row=2, column=0, columnspan=2)

def undo_pembayaran(user):
    if not undo_stack:
        messagebox.showinfo("Undo", "Tidak ada transaksi.")
        return
    last = undo_stack.pop()
    nim, jumlah, tanggal = last['nim'], last['jumlah'], last['tanggal']

    mahasiswa[nim]['riwayat'] = [r for r in mahasiswa[nim]['riwayat']
                                 if not (r['jumlah'] == jumlah and r['tanggal'] == tanggal)]
    simpan_mahasiswa()

    rows = []
    with open(FILE_KAS, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['NIM'] == nim and row['Jumlah'] == str(jumlah) and row['Tanggal'] == tanggal:
                continue
            rows.append(row)
    with open(FILE_KAS, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['NIM', 'Nama', 'Kelas', 'Jumlah', 'Tanggal'])
        writer.writeheader()
        writer.writerows(rows)

    tulis_log(user, f"Undo pembayaran Rp{jumlah} oleh {nim}")
    messagebox.showinfo("Undo", f"Pembayaran {nim} dibatalkan.")

def tampil_tabel():
    win = tk.Toplevel()
    win.title("Tabel Mahasiswa")
    from database import mahasiswa

    tree = ttk.Treeview(win)
    tree["columns"] = ("NIM", "Nama", "Kelas", "Bayar", "Tunggakan")
    tree.column("#0", width=0, stretch=tk.NO)
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="w", width=150)
    tree.pack(expand=True, fill='both')

    def isi_data():
        for i in tree.get_children():
            tree.delete(i)
        load_mahasiswa()
        load_tunggakan()
        for nim, data in mahasiswa.items():
            tree.insert("", "end", values=(
                nim,
                data['nama'],
                data['kelas'],
                f"Rp{total_bayar(nim):,}",
                f"Rp{sisa_tunggakan(nim):,}"
            ))

    tk.Button(win, text="Refresh", command=isi_data).pack(pady=5)
    isi_data()

def riwayat_bayar():
    win = tk.Toplevel()
    win.title("Riwayat")

    tk.Label(win, text="NIM").pack()
    entry = tk.Entry(win)
    entry.pack()
    box = tk.Text(win, height=10, width=50)
    box.pack()

    def tampil():
        nim = entry.get()
        if nim not in mahasiswa:
            messagebox.showerror("Gagal", "Tidak ditemukan.")
            return
        box.delete("1.0", tk.END)
        for r in mahasiswa[nim]['riwayat']:
            box.insert(tk.END, f"- Rp{r['jumlah']:,} pada {r['tanggal']}\n")

    def refresh():
        load_mahasiswa()
        tulis_log("admin", "Refresh data riwayat")
        messagebox.showinfo("Refresh", "Data dimuat.")

    tk.Button(win, text="Lihat", command=tampil).pack(pady=2)
    tk.Button(win, text="Refresh", command=refresh).pack()

def tambah_tunggakan(user):
    win = tk.Toplevel()
    win.title("Tambah Tunggakan")

    tk.Label(win, text="Nominal").grid(row=0, column=0)
    nominal = tk.Entry(win)
    nominal.grid(row=0, column=1)

    def tambah():
        try:
            nilai = int(nominal.get())
        except:
            messagebox.showerror("Error", "Input harus angka.")
            return
        from database import tunggakan_histori
        tunggakan_histori.append(nilai)
        tulis_log(user, f"Tunggakan global Rp{nilai}")
        messagebox.showinfo("Sukses", f"Tunggakan Rp{nilai} ditambahkan.")
        win.destroy()

    tk.Button(win, text="Tambah", command=tambah).grid(row=1, column=0, columnspan=2)

def total_kas():
    total = 0
    if os.path.exists(FILE_KAS):
        with open(FILE_KAS, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += int(row['Jumlah'])
    messagebox.showinfo("Total Kas", f"Total kas masuk: Rp{total:,}")

def refresh_data():
    load_mahasiswa()
    load_tunggakan()
    messagebox.showinfo("Refresh", "Data berhasil dimuat ulang.")
