import csv
import os

FILE_ADMIN = "data/admin.csv"

def login_admin(username, password):
    if not os.path.exists(FILE_ADMIN):
        return False
    with open(FILE_ADMIN, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False
