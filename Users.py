from pydb import Pydb, Query
from faker import Faker

fake = Faker() # pip install faker required 
db = Pydb(connection="Users.json")
User = Query(db)

# insert random faker data
for x in range(101):
    db.insert({
        "name": str(fake.name()),
        "age": int(fake.random_number(digits=2)),
        "fav_letter": str(fake.random_uppercase_letter())
    })
    
# write your own query and statements and see the results 😊

print(db.all())
