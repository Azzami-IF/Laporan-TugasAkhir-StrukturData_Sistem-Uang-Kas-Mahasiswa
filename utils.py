import csv
from datetime import datetime

FILE_LOG = "data/log.csv"

def tulis_log(user, aksi):
    waktu = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(FILE_LOG, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([waktu, user, aksi])

from database import mahasiswa, tunggakan_histori

def total_tagihan():
    return sum(tunggakan_histori)

def total_bayar(nim):
    return sum([r['jumlah'] for r in mahasiswa[nim]['riwayat']])

def sisa_tunggakan(nim):
    return max(0, total_tagihan() - total_bayar(nim))
