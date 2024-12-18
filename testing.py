import pandas as pd
import re

# Load the CSV file
file_path = 'data.csv'  # Replace with the actual path to your file
df = pd.read_csv(file_path)

# Expanded dictionary with company names and their NASDAQ symbols
company_symbols = {
    "Meta": "META",
    "Facebook": "META",
    "STMicro": "STM",
    "Autodesk": "ADSK",
    "Prosus": "PROSY",
    "Naspers": "NPSNY",
    "Google": "GOOGL",
    "Alphabet": "GOOGL",
    "Nvidia": "NVDA",
    "Trend Micro": "TMICY",
    "TikTok": "BDNCE",
    "Live Nation": "LYV",
    "Apple": "AAPL",
    "Tesla": "TSLA",
    "Microsoft": "MSFT",
    "Dell": "DELL",
    "Amazon": "AMZN",
    "OpenAI": "MSFT"
}

def find_stock_symbol(title):
    for company, symbol in company_symbols.items():
        # Use regular expressions for a case-insensitive search
        if re.search(r'\b' + re.escape(company) + r'\b', title, re.IGNORECASE):
            return symbol
    return None

# Apply the function to the 'title' column to create a new 'stock_symbol' column
df['stock_symbol'] = df['title'].apply(find_stock_symbol)

# Save the updated dataframe to a new CSV file
output_file_path = 'data_symbol.csv'  # Replace with the desired output path
df.dropna(inplace=True)
df.to_csv(output_file_path, index=False)

print(df.head())
