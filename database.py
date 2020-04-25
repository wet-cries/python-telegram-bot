import sqlite3
import config
DB = 'database.db'

def set_state(user_id, value):
	conn = sqlite3.connect(DB)
	c = conn.cursor()
	c.execute("UPDATE state SET state = ? WHERE user_id = ?", (value, str(user_id),))
	conn.commit()
	conn.close()

def get_state(user_id):
	conn = sqlite3.connect(DB)
	c = conn.cursor()
	try:
		c.execute("SELECT state FROM state WHERE user_id = ?", (str(user_id),))
		row = c.fetchone()
		out = "%s" % (row[0])
		conn.close()
		return out
	except TypeError:
		c.execute("INSERT INTO state VALUES (?, ?)", (str(user_id), '0',))
		conn.commit()
		conn.close()
		return config.States.S_START.value		
		


