import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('my_database.db')

# Query the data
query = "SELECT * FROM predictions"
df = pd.read_sql_query(query, conn)

# Display the data
print(df)

# Close the connection
conn.close()
