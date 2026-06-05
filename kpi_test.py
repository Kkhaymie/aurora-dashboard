import pandas as pd

# Sales metrics — deduplicate since each transaction repeats 4x (one per dept)
sales_df = pd.read_csv("aurora_clean.csv").drop_duplicates(subset='transaction_id')

total_revenue = sales_df['revenue'].sum()
total_profit = sales_df['profit'].sum()
profit_margin = (total_profit / total_revenue) * 100

# Budget metrics — use full df (each row = one dept's budget)
budget_df = pd.read_csv("aurora_clean.csv")
total_budgeted = budget_df['budgeted_revenue'].sum()
total_actual = budget_df['actual_revenue'].sum()
budget_variance_pct = ((total_actual - total_budgeted) / total_budgeted) * 100

# Revenue by Region and Channel
revenue_by_region = sales_df.groupby('region')['revenue'].sum().reset_index()
revenue_by_channel = sales_df.groupby('channel')['revenue'].sum().reset_index()

# Churn Rate
churn_rate = (sales_df['churn_flag'].value_counts(normalize=True).get('Yes', 0)) * 100

print(f"Total Revenue:     ${total_revenue:,.0f}")
print(f"Total Profit:      ${total_profit:,.0f}")
print(f"Profit Margin:     {profit_margin:.1f}%")
print(f"Budget Variance:   {budget_variance_pct:+.1f}%")
print(f"Churn Rate:        {churn_rate:.1f}%")
print(f"\nRevenue by Region:\n{revenue_by_region}")
print(f"\nRevenue by Channel:\n{revenue_by_channel}")