import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',  
    password='',  
    database='manajemen_pengguna'
)

print("Koneksi berhasil!")
connection.close()
