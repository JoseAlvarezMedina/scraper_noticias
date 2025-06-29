import sqlite3

conn = sqlite3.connect('noticias.db')
count = conn.execute('SELECT COUNT(*) FROM noticias').fetchone()[0]
print(f"Total artículos: {count}")
conn.close()
