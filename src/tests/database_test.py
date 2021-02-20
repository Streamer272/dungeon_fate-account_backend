from DatabaseController import *

db = DatabaseController("licences.sql")

print(db.get_table("licences"))

for license_ in db.get_table("licences"):
    print(type(license_[0]))
    print(type(license_[1]))
