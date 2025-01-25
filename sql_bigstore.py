import sqlite3
import pandas as pd
import cProfile

df = pd.read_csv('scanner_data.csv')
#clean the data

df.drop_duplicates(inplace=True)
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df[df['Date'].notna()]

#Filter rows with invalid or missing Customer_ID and Transaction_ID
df = df[(df['Customer_ID'].notna()) & (df['Transaction_ID'].notna())]
df = df[(df['Customer_ID'] > 0) & (df['Transaction_ID'] > 0)]

# Ensure SKU and SKU_Category are valid
df = df[df['SKU_Category'].notna() & df['SKU_Category'].str.strip() != ""]
df = df[df['SKU'].notna() & df['SKU'].str.strip() != ""]

#  Validate Quantity (must be positive)
df = df[df['Quantity'] > 0]
df = df[df['Sales_Amount'] > 0]

df.to_csv('cleaned_scanner_data.csv', index=False)

print (df.head())

# set up database

conn = sqlite3.connect('big_store.db')
cursor = conn.cursor()

data = pd.read_csv('cleaned_scanner_data.csv')

# Write DataFrame to the database
data.to_sql('transactions', conn, if_exists='replace', index=False)


def run_query():
    # Define queries
    queries = {
        "daily_sales": """
            SELECT Date, SUM(Quantity) AS Total_Quantity, SUM(Sales_Amount) AS Daily_Sales
            FROM transactions
            GROUP BY Date
            ORDER BY Date;
        """,
        "customer_spending": """
            SELECT Customer_ID, SUM(Sales_Amount) AS Total_Spent
            FROM transactions
            GROUP BY Customer_ID
            ORDER BY Total_Spent DESC;
        """,
        "product_sales": """
            SELECT SKU, SUM(Quantity) AS Total_Quantity, SUM(Sales_Amount) AS Total_Sales
            FROM transactions
            GROUP BY SKU
            ORDER BY Total_Quantity DESC;
        """
    }

    # Run each query and save results to CSV
    for name, query in queries.items():
        # Execute the query
        result = pd.read_sql_query(query, conn)

        # Save the result to a CSV file
        csv_filename = f"{name}.csv"
        result.to_csv(csv_filename, index=False)
        print(f"Query '{name}' saved to {csv_filename}")

    # Close the database connection
    conn.close()

# Profile the function
cProfile.run('run_query()')