
from interface import Database

db = Database("db.sqlite")


db.exec("""
INSERT INTO customers(cid, username, full_name, location, phone_number, email)
VALUES (0, 'a', 'a', 'a', 'a', 'a')
""")
db.exec("""
INSERT INTO customers(cid, username, full_name, location, phone_number, email)
VALUES (1, 'a', 'b', 'a', 'a', 'a')
""")

print(db.query("""
SELECT * FROM customers
"""))

