import sqlite3

conn = sqlite3.connect("flights.sqlite3")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
conn.close()
