![PYDB_logo](image/logo.svg)

## Table of Contents  
- [Disclaimer](#Disclaimer)  
- [SQL equivalent restructuring filter](#SQL-equivalent-restructuring-filter) 
- [SQL equivalent statements](#SQL-equivalent-statements) 

## Disclaimer
**This is a proof of concept**. I developed this project to challenge myself learn about the internals of databases, software design and object oriented programming.

## Sample usage
```python
from pydb import Pydb, Query

db = Pydb(connection="Users.json", tablename="Users")
Student = Query(db)

print(db.length()) # int: number of columns

db.filter(User.name == "Yusuf")

print(db.all()) 
# List[Dict[str, Any]]: return columns where 
# that include -> {"name": "Yusuf"}

db.filter(User.age != 16)

print(db.all()) 
# List[Dict[str, Any]]: return table where 
# that don't include -> {"age": 16}

```
## SQL equivalent restructuring filter
### ALL
return result of query or whole table
```python
db.filter(User.name == "Yusuf")
print(db.all()) 
# List[Dict[str, Any]]: return columns where 
# that include -> {"name": 16} and limit to 5 return columns
```
### LIMIT
return columns to a specific limit
```python
db.filter(User.age == 16)
print(db.limit(5)) 
# List[Dict[str, Any]]: return columns where 
# that include -> {"age": 16} and limit to 5 return columns
```
### ASC
Note: this is the natural order.
```python
db.filter(User.name == "Yusuf")
print(db.asc()) 
# List[Dict[str, Any]]: return columns where 
# that include -> {"name": "Yusuf"} 
```
### DESC
reverse of natural order
```python
db.filter(User.name == "Yusuf")

print(db.desc()) 
# List[Dict[str, Any]]: return columns where 
# that include -> {"name": "Yusuf"} and desc order
```

## SQL equivalent statements
### SELECTALL
Equivalent to SELECT * FROM _TABLENAME_;<br>
returns a result table
```python
db.selectall()
```
### SELECT
Equivalent to SELECT column1, ... FROM _TABLENAME_;<br>
returns columns the include specified keys
```python
db.select(["name"])
```
### INSERT
Insert new column into database
```python
db.insert({"name": "Yusuf", "age": 16,
        "money": None, "Python": True
        "Java": False})
```
### UPDATE
UPDATE table_name SET _column1_=_'value1'_, ... WHERE _column1_=_'value1'_;
Update specific column(s) <br>
```python
db.update({"seal": True}, {"name": "Yusuf"})
# add {"seal": True} where {"name": "Yusuf"}
```
### DROP
DROP DATABASE _TABLENAME_;
This command is **irreversible**
```python
db.drop()
```
### DELETE
Equivalent to DELETE FROM _TABLENAME_ WHERE _KEY_=_'VALUE'_;<br>
Drop all columns with same key and value
```python
db.delete({"name": "Yusuf"})
```

