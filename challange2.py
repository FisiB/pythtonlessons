import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dt = pd.read_csv("weather_tokyo_data.csv")

print(dt['temperature'].dtype)

temperature_column = pd.to_numeric(dt['temperature'], errors='coerce')

temperature_column = temperature_column.dropna()

temp_avg = np.mean(temperature_column)

print(f"Average temperature: {temp_avg:.2f}")

dt = pd.read_csv("weather_tokyo_data.csv", names=['year', 'day', 'temperature', 'humidity', 'atmospheric_pressure'], header=None)

dt['date'] = pd.to_datetime(dt['year'].astype(str) + '-' + dt['day'], format='%Y-%m/%d', errors='coerce')

dt['temperature'] = pd.to_numeric(dt['temperature'], errors='coerce')
dt = dt.dropna(subset=['date', 'temperature'])

dt['month'] = dt['date'].dt.month
dt['year_month'] = dt['date'].dt.to_period('M')

def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

dt['season'] = dt['month'].apply(get_season)

seasonal_avg = dt.groupby('season')[['temperature']].mean()

print("Seasonal average temperatures:")
print(seasonal_avg)

plt.figure(figsize=(10, 6))
seasonal_avg['temperature'].plot(kind='line', marker='o', color='b', linestyle='-', linewidth=2)

plt.title('Average Temperature per Season in Tokyo', fontsize=16)
plt.xlabel('Season', fontsize=14)
plt.ylabel('Average Temperature (°C)', fontsize=14)

plt.xticks(rotation=45)
plt.tight_layout()  
plt.show()
monthly_avg = dt.groupby('year_month')[['temperature']].mean()

print("Monthly average temperatures:")
print(monthly_avg)

hottest_day = dt.loc[dt['temperature'].idxmax()]
coldest_day = dt.loc[dt['temperature'].idxmin()]

print(f"\nHottest day:")
print(f"Date: {hottest_day['date']} | Temperature: {hottest_day['temperature']}°C")

print(f"\nColdest day:")
print(f"Date: {coldest_day['date']} | Temperature: {coldest_day['temperature']}°C")

plt.figure(figsize=(10, 6))
monthly_avg['temperature'].plot(kind='bar', color='skyblue', edgecolor='black')

plt.title('Monthly Average Temperature in Tokyo', fontsize=16)
plt.xlabel('Month-Year', fontsize=14)
plt.ylabel('Average Temperature (°C)', fontsize=14)

plt.xticks(rotation=45, ha='right')
plt.tight_layout()  
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(dt['date'], dt['temperature'], color='b', linestyle='-', linewidth=1.5)

plt.title('Temperature Changes Over Time in Tokyo', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Temperature (°C)', fontsize=14)

plt.xticks(rotation=45, ha='right')

plt.tight_layout()  
plt.show()