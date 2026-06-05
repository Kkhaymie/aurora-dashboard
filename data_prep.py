import pandas as pd

df = pd.read_csv("aurora_full_dataset.csv")

# Dates are already proper strings in the CSV - just parse them directly
df['transaction_date'] = pd.to_datetime(df['transaction_date'])
df['signup_date'] = pd.to_datetime(df['signup_date'])

# Extract year and month
df['year'] = df['transaction_date'].dt.year
df['month'] = df['transaction_date'].dt.to_period('M').astype(str)

# Save cleaned version
df.to_csv("aurora_clean.csv", index=False)
print("Done. Shape:", df.shape)