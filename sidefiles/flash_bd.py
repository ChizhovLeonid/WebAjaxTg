import sqlite3

with open('bin_files/checkboxes.txt', 'r', encoding='utf-8') as file:
    checkboxes = [line.strip() for line in file]

conn = sqlite3.connect('bin_files/checkboxes.db', check_same_thread=False)
cursor = conn.cursor()

values = []
names = []
for checkbox in checkboxes:
    names.append(checkbox)
    values.append(0)
    
query = "INSERT INTO checkboxes_vasya ({})".format(", ".join(map(str, names)))  + " VALUES ({})".format(", ".join(map(str, values)))
cursor.execute(query)
conn.commit()
 
query = "INSERT INTO checkboxes_petya ({})".format(", ".join(map(str, names)))  + " VALUES ({})".format(", ".join(map(str, values)))
cursor.execute(query)
conn.commit()