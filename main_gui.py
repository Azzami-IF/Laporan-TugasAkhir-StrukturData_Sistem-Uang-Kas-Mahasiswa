import tkinter as tk
from tkinter import messagebox, ttk
from auth import login_admin
from logic import *
from database import load_mahasiswa, load_tunggakan
from utils import tulis_log

class KasApp:
    def __init__(self, root):
        self.root = root
        self.username = None
        self.login_window()

    def login_window(self):
        self.root.title("Login Admin")
        tk.Label(self.root, text="Username").grid(row=0, column=0)
        tk.Label(self.root, text="Password").grid(row=1, column=0)
        self.user_entry = tk.Entry(self.root)
        self.pass_entry = tk.Entry(self.root, show="*")
        self.user_entry.grid(row=0, column=1)
        self.pass_entry.grid(row=1, column=1)
        tk.Button(self.root, text="Login", command=self.login).grid(row=2, column=0, columnspan=2)

    def login(self):
        u = self.user_entry.get()
        p = self.pass_entry.get()
        if login_admin(u, p):
            self.username = u
            tulis_log(u, "Login berhasil")
            self.root.destroy()
            self.main_window()
        else:
            messagebox.showerror("Login Gagal", "Username/password salah.")

    def main_window(self):
        load_mahasiswa()
        load_tunggakan()

        self.root = tk.Tk()
        self.root.title("Sistem Uang Kas Mahasiswa")

        btns = [
            ("Tambah Mahasiswa", lambda: tambah_mahasiswa(self.username)),
            ("Hapus Mahasiswa", lambda: hapus_mahasiswa(self.username)),
            ("Pembayaran Kas", lambda: bayar_kas(self.username)),
            ("Undo Pembayaran Terakhir", lambda: undo_pembayaran(self.username)),
            ("Tampilkan Tabel Mahasiswa", tampil_tabel),
            ("Riwayat Pembayaran", riwayat_bayar),
            ("Tambah Tunggakan", lambda: tambah_tunggakan(self.username)),
            ("Total Uang Kas", total_kas),
            ("Refresh Data", refresh_data),
            ("Keluar", self.root.quit),
        ]
        for i, (text, cmd) in enumerate(btns):
            tk.Button(self.root, text=text, width=30, command=cmd).grid(row=i, column=0, pady=3, padx=10)

        self.root.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    app = KasApp(root)
    root.mainloop()
