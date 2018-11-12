
import sqlite3

db = sqlite3.connect("db.sqlite")

cursor = db.cursor()


db.close()