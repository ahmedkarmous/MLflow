import psycopg2
from prettytable import PrettyTable

# URL to connect to the db
DB_URL = "postgresql://user:password@localhost:5432/mlflowdb"

# Connect to the db
conn = psycopg2.connect(DB_URL)



cur = conn.cursor()
# Queries
cur = conn.cursor()
cur.execute("SELECT * FROM RUNS;")
rows = cur.fetchall()

table = PrettyTable()
table.field_names = [desc[0] for desc in cur.description]  # Noms des colonnes

for row in rows:
    table.add_row(row)

print(table)

# cur.execute("INSERT INTO EXPERIMENTS (name) VALUES ('test_insertion')")

cur.close()
conn.close()