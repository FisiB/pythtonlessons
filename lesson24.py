import sqlite3

connection = sqlite3.connect('example.db')

cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT NOT NULL,
        department TEXT NOT NULL,
        salary REAL
    )''')

connection.commit()

cursor.execute('''
INSERT INTO employees (name, position, department, salary)
VALUES(?,?,?,?)
''', ('John', 'Software Engineer', 'IT', '70000.00'))

connection.commit()

cursor.execute('SELECT * FROM employees')
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute('''
UPDATE employees
SET salary = ?
WHERE name = ?
               
''', ('75000.00', 'John'))

connection.commit()

cursor.execute('''
DELETE FROM employees
WHERE name = ?    
''', ('John',))
connection.commit

cursor.close()
connection.close()