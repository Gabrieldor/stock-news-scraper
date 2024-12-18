import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("data.csv")

df['date'] = pd.to_datetime(df['date'])

# Extract the date part (without time)
df['day'] = df['date'].dt.date

grouped = df.groupby('day')

# Initialize lists to store relative prices
min_to_open_ratios = []
max_to_open_ratios = []

# Iterate over each group (each day)
for day, group in grouped:
    open_price = group['open'].iloc[0]
    max_price = group['max'].max()
    min_price = group['min'].min()
    
    min_to_open_ratios.append((min_price / open_price) * 100)
    max_to_open_ratios.append((max_price / open_price) * 100)

# Calculate the average relative prices
average_min_to_open = sum(min_to_open_ratios) / len(min_to_open_ratios)
average_max_to_open = sum(max_to_open_ratios) / len(max_to_open_ratios)

# Print the results
print(f"Average Minimum to Open Price Ratio: {average_min_to_open:.2f}%")
print(f"Average Maximum to Open Price Ratio: {average_max_to_open:.2f}%")