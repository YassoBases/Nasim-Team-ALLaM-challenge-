import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# List all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print the tables found in the database
print("Tables in the database:", tables)

# Close the connection to the database
conn.close()
