#ctrl+alt+shitf+insert para scratch file

import sqlite3

conn = sqlite3.connect("Componentes.db")
cursor = conn.cursor()


cursor.execute('SELECT * FROM fontes')
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()

