import time
from pydb import Pydb, Query
import random
import time
#from faker import Faker

#fake = Faker() # pip install faker required 
db = Pydb(connection="Users.json")
User = Query(db)

start = time.time()
#insert random faker data
for x in range(101):
    db.insert({
        "name": "Yusuf",
        "age": "16",
        "fav_letter": int(random.random())
    })
    
print(round(time.time() - start, 4))
 
# write your own query and statements and see the results 😊

# insert - no mmap - 100 insert - 0.0988 secs 
# insert - no mmap - 1000 insert - 9.0446 secs 

#print(db.all())




