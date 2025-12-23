import pandas as pd
from database import get_connection

df = pd.read_csv("../data/players.csv")

conn = get_connection()
df.to_sql("players", conn, if_exists="replace", index=False)
conn.close()

print("Players data loaded successfully")
