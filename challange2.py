import numpy as np
import pandas as pd

dt = pd.read_csv("weather_tokyo_data.csv")

print(dt['temperature'].dtype)

temperature_column = pd.to_numeric(dt['temperature'], errors='coerce')

temperature_column = temperature_column.dropna()

temp_avg = np.mean(temperature_column)

print(f"Average temperature: {temp_avg:.2f}")

dt['day'] = pd.to_datetime(dt['day'], errors='coerce')

dt['month'] = dt['day'].dt.month

dt['temperature'] = pd.to_numeric(dt['temperature'], errors='coerce')

df = dt.dropna(subset=['temperature', 'month'])

monthly_avg = dt.groupby('month')['temperature'].mean()

monthly_avg.index = monthly_avg.index.map(lambda x: pd.to_datetime(str(x), format='%m').strftime('%B'))

print("Monthly average temperatures:")
print(monthly_avg)