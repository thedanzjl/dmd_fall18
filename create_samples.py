import random
import string
from interface import Database

db = Database("db.sqlite")
db.clear_all()


# INSERTING CUSTOMER'S SAMPLES
N = 10

names = ['Daniel', 'Roman', 'Mary', 'Nikolay', 'Vladimir']
locations = ['Barbara street 1337', 'Universitetskaya 1', 'Sportivnaya 3']

chars = string.printable[:62]
usernames = list()
for _ in range(N):  # generate random usernames
    username = ''
    for i in range(random.randint(5, 10)):
        username += random.choice(chars)
    usernames.append(username)


for id in range(N):
    username = usernames[id]
    full_name = random.choice(names)
    location = random.choice(locations)
    phone_number = ''.join([random.choice('0123456789') for i in range(11)])
    email = username + random.choice(['@mail.ru', '@gmail.com', '@innopolis.ru', '@bk.ru'])

    db.insert_into('customers', cid=id, username=username, full_name=full_name, location=location,
                phone_number=phone_number, email=email)

# INSERTING CARS SAMPLES

# INSERTING RIDES SAMPLES

# INSERTING PLUG_TYPES SAMPLES

# INSERTING CHARGING_STATIONS SAMPLES

# INSERTING CAR_PART_TYPES SAMPLES

# INSERTING PROVIDERS SAMPLES

# INSERTING WORKSHOPS SAMPLES

# INSERTING RELATIONSHIPS WORKSHOPS-HAVE-CAR_PARTS

# INSERTING RELATIONSHIPS PROVIDERS-PROVIDE-CAR_PARTS

# INSERTING RELATIONSHIPS CARS-HAVE-CAR_PART

# INSERTING RELATIONSHIPS CHARGING_STATIONS-SUITS-PLUG_TYPES


if __name__ == '__main__':
    print(db.query("""
    SELECT * FROM customers
    """))

