#ctrl+alt+shitf+insert para scratch file

import sqlite3

conn = sqlite3.connect("Componentes.db")
cursor = conn.cursor()

cursor.execute(f"DROP TABLE IF EXISTS 'processadores'")

sql = f'''CREATE TABLE "processadores"(
        nome,
        preco,
        socket,
        freq_base,
        freq_boost,
        nucleos,
        threads,
        tdp,
        cooler,
        imgnome,
        id,
        urlpr
    )'''

cursor.execute(f"DROP TABLE IF EXISTS 'graficas'")

sql2 = f'''CREATE TABLE "graficas"(
        nome,
        preco,
        memoria,
        cuda,
        directX,
        openGL,
        imgnome,
        id,
        tdp,
        urlpr
    )'''
cursor.execute(f"DROP TABLE IF EXISTS 'motherboards'")

sql3 = f'''CREATE TABLE "motherboards"(
        nome,
        preco,
        socket,
        chipset,
        ddr,
        imgnome,
        id,
        urlpr
    )'''

cursor.execute(f"DROP TABLE IF EXISTS 'ram'")

sql4 = f'''CREATE TABLE "ram"(
        nome,
        preco,
        capacidade,
        tipo,
        velocidade,
        latencia,
        imgnome,
        id,
        tdp,
        urlpr
    )'''

cursor.execute(f"DROP TABLE IF EXISTS 'fontes'")

sql5 = f'''CREATE TABLE "fontes"(
        nome,
        preco,
        max_cap,
        efic,
        imgnome,
        id,
        tdp,
        urlpr
    )'''

cursor.execute(sql)
print("Table created successfully........")

cursor.execute(sql2)
print("Table created successfully........")

cursor.execute(sql3)
print("Table created successfully........")

cursor.execute(sql4)
print("Table created successfully........")

cursor.execute(sql5)
print("Table created successfully........")

conn.commit()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

conn.close()
