import numpy as np
import pandas as pd

dt = pd.read_csv("weather_tokyo_data.csv")

print(dt['temperature'].dtype)

temperature_column = pd.to_numeric(dt['temperature'], errors='coerce')

temperature_column = temperature_column.dropna()

temp_avg = np.mean(temperature_column)

print(f"Average temperature: {temp_avg:.2f}")

import pandas as pd


dt = pd.read_csv("weather_tokyo_data.csv", names=['year', 'day', 'temperature', 'humidity', 'atmospheric_pressure'], header=None)


dt['date'] = pd.to_datetime(dt['year'].astype(str) + '-' + dt['day'], format='%Y-%m/%d', errors='coerce')


dt['temperature'] = pd.to_numeric(dt['temperature'], errors='coerce')

dt = dt.dropna(subset=['date', 'temperature'])

dt['month'] = dt['date'].dt.month
dt['year_month'] = dt['date'].dt.to_period('M')

monthly_avg = dt.groupby('year_month')[['temperature']].mean()

print("Monthly average values:")
print(monthly_avg)
