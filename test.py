import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
'''
for row in c.execute("SELECT * FROM state"):
	print(row)
'''
c.execute("ALTER TABLE state ALTER COLUMN user_id int") 

c.close()
conn.close()
