import csv, os
from datetime import datetime

FILE_MHS = "data/data_mahasiswa.csv"
FILE_KAS = "data/kas_mahasiswa.csv"
FILE_LOG = "data/log.csv"

mahasiswa = {}
tunggakan_histori = []

def load_mahasiswa():
    mahasiswa.clear()
    if os.path.exists(FILE_MHS):
        with open(FILE_MHS, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                mahasiswa[row['NIM']] = {
                    'nama': row['Nama'],
                    'kelas': row['Kelas'],
                    'riwayat': []
                }
    if os.path.exists(FILE_KAS):
        with open(FILE_KAS, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                nim = row['NIM']
                if nim in mahasiswa:
                    mahasiswa[nim]['riwayat'].append({
                        'jumlah': int(row['Jumlah']),
                        'tanggal': row['Tanggal']
                    })

def simpan_mahasiswa():
    with open(FILE_MHS, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['NIM', 'Nama', 'Kelas'])
        for nim, data in mahasiswa.items():
            writer.writerow([nim, data['nama'], data['kelas']])

def simpan_pembayaran(nim, jumlah):
    tanggal = datetime.now().strftime('%Y-%m-%d')
    data = mahasiswa[nim]
    with open(FILE_KAS, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([nim, data['nama'], data['kelas'], jumlah, tanggal])

def load_tunggakan():
    tunggakan_histori.clear()
    if os.path.exists(FILE_LOG):
        with open(FILE_LOG, newline='') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if "Tunggakan global Rp" in row[2]:
                    nominal = int(row[2].split("Rp")[1])
                    tunggakan_histori.append(nominal)
