import mysql.connector

class dbHandle:
	def checkDB():
		try:
			db = mysql.connector.connect(user="root", password="", host="localhost", database="users")
			return True
		except mysql.connector.Error as err:
			e = format(err)
			print(e)
			return False

	def createDB():
		#if db exists do not query
		if (checkDB()):
			return True
		else:
			try:
				db = mysql.connector.connect(user="root", password="", host="localhost", database="users")
				mycursor = db.cursor()
				mycursor.execute("CREATE DATABASE IF NOT EXISTS users")
			except mysql.connector.Error as err:
				e = format(err)
				print(e)


	def create_table():
		db = mysql.connector.connect(user="root", password="", host="localhost", database="users")
		mycursor = db.cursor()
		mycursor.execute("CREATE TABLE IF NOT EXISTS user_info (id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(255), password VARCHAR(255))")

	def insert_info(username,password):
		db = mysql.connector.connect(user="root", password="", host="localhost", database="users")
		mycursor = db.cursor()
		sql = "INSERT INTO user_info (username, password) VALUES (%s, %s)"
		val = (username,password)
		mycursor.execute(sql, val)
		db.commit()
		print(mycursor.rowcount, "record inserted.")

	def select_info(name, pas):
		db = mysql.connector.connect(user="root", password="", host="localhost", database="users")
		mycursor = db.cursor()
		mycursor.execute("SELECT * FROM user_info WHERE username = '" + name + "' AND password = '" + pas + "'")
		record = mycursor.fetchone()
		if record:
			#print(record)
			return True
		else:
			print(record)
			return False

	def insert_user(name, pas):
		#master_key = Fernet.generate_key()
		#pas = cipher_method(master_key, pas)
		db = mysql.connector.connect(user="root", password="", host="localhost", database="users")
		mycursor = db.cursor()
		#mycursor.execute("INSERT INTO user_info (username, password) VALUES (%s, %s)", ("Kelly", "123"))
		mycursor.execute("INSERT INTO user_info (username, password) VALUES('" + name + "','" + pas + "')")
		db.commit()
		print(mycursor.rowcount, "record inserted.")