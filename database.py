# import sqlite3

# # Connect to the database (or create it if it doesn't exist)
# connection = sqlite3.connect('example.db')

# # Create a cursor object to interact with the database
# cursor = connection.cursor()

# # Create a table named 'employees'
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS employees (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     position TEXT NOT NULL,
#     department TEXT NOT NULL,
#     salary REAL
# )
# ''')

# # Commit the changes
# connection.commit()

# # Insert a new employee
# cursor.execute('''
# INSERT INTO employees (name, position, department, salary)
# VALUES (?, ?, ?, ?)
# ''', ('John Doe', 'Software Engineer', 'IT', 70000.00))

# # Commit the changes
# connection.commit()

# # Select all employees
# cursor.execute('SELECT * FROM employees')

# # Fetch all results
# rows = cursor.fetchall()

# for row in rows:
#     print(row)

# # Update the salary of an employee
# cursor.execute('''
# UPDATE employees
# SET salary = ?
# WHERE name = ?
# ''', (75000.00, 'John Doe'))

# # Commit the changes
# connection.commit()

# # Delete an employee
# cursor.execute('''
# DELETE FROM employees
# WHERE name = ?
# ''', ('John Doe',))

# # Commit the changes
# connection.commit()

# # Close the cursor and connection
# cursor.close()
# connection.close()