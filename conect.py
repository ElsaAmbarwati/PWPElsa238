import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',  # Ganti dengan username Anda
    password='',  # Ganti dengan password Anda
    database='manajemen_pengguna'
)

print("Koneksi berhasil!")
connection.close()
