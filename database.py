import sqlite3

connection = sqlite3.connect("garry_food.db")
sql = connection.cursor()

sql.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER, name TEXT, phone_number TEXT);")

def add_user(user_id, name, phone_number):
    connection = sqlite3.connect("garry_food.db")
    sql = connection.cursor()
    sql.execute("INSERT INTO users (user_id, name, phone_number)"
                "VALUES (?,?,?);", (user_id, name, phone_number) )
    connection.commit()
