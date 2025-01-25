from transaction import Transaction
from cProfile import Profile
from pstats import SortKey, Stats
from collections import deque
from customer import  Customer,Purchase
import pandas as pd



def process_scanner_data_DO_NOT_PROFILE(file_path):
    """
    Process the scanner_data.csv file and create Transaction objects for each valid row.

    Args:
        file_path (str): The path to the scanner_data.csv file.

    Returns:
        list: A list of Transaction objects created from the CSV file.
    """
    transactions = [ ]
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                # Strip leading/trailing whitespace
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                # Skip header (assuming it's the first line)
                if line_number == 1 and line.startswith("ID,Date,Customer_ID"):
                    continue

                try:
                    transaction = Transaction.from_csv_row(line)
                    transactions.append(transaction)
                except ValueError as e:
                    print(f"Error processing line {line_number}: {e}")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred while processing the file: {e}")

    return transactions


#-------------------------------------------------------------------------------------------------------------------
def create_transactions_dataframe(transactions):
        """
        Convert the transactions list into a pandas DataFrame.

        Args:
            transactions (list): A list of transaction objects.

        Returns:
            pd.DataFrame: A DataFrame containing the transaction data.
        """
        data = {
            "Date": [trans.Date for trans in transactions],
            "Customer_ID": [trans.Customer_ID for trans in transactions],
            "Product": [trans.product for trans in transactions],
            "Quantity": [int(trans.Quantity) for trans in transactions],
            "Sales_Amount": [float(trans.Sales_Amount) for trans in transactions]
        }
        return pd.DataFrame(data)


def process_best_selling_product( transactions  )->str:
    header = "# Best products by sales (product, sales)  \n"
    r = report_best_selling_products( transactions )
    return header + r


def report_best_selling_products(df)-> str:
    # Group by product and calculate total quantity and sales
    # DataFrame.groupby(by=None, axis=<no_default>, level=None, as_index=True, sort=True, group_keys=True, observed=<no_default>, dropna=True)
    grouped = df.groupby(by="Product", as_index=False).agg(  # groups all rows in df that have the same value in the "Product" column.
        Total_Quantity=("Quantity", "sum"),                 #Adds up the "Quantity" column for each product group
        Total_Sales=("Sales_Amount", "sum")                 #Does the same but for sales
    )

    # Sort by total quantity in descending order
    sorted_grouped = grouped.sort_values(by="Total_Quantity", ascending=False) #best selling products at top of list

    # Format the results into a string
    result = f"# number of products sold = {len(sorted_grouped)}\n" #building block for iteration of sorted_grouped
    for _, row in sorted_grouped.iterrows():
        result += f"|{row['Product']}|{row['Total_Quantity']:.0f}|£{row['Total_Sales']:.2f}\n"

    return result


#----------------------------------------------------------------
def report_daily_sales( transactions) ->str:
    assert transactions is not None , "No null transaction lists processed "
    header = "# Best products by sales (product, sales)  \n"
    r = process_daily_sales( transactions )
    return  header + r


def process_daily_sales(df) ->str:
    # Group by date and calculate total quantity and sales
    grouped = df.groupby("Date", as_index=False).agg(
        Total_Quantity=("Quantity", "sum"),
        Total_Sales=("Sales_Amount", "sum")
    )

    # Sort by total quantity in descending order
    sorted_grouped = grouped.sort_values(by="Total_Quantity", ascending=False)

    # Format the results into a string
    result = f"# number of days = {len(sorted_grouped)}\n"
    for _, row in sorted_grouped.iterrows():
        result += f"|{row['Date']}|{row['Total_Quantity']:.0f}|£{row['Total_Sales']:.2f}|\n"

    return result

#==============================================================================
def report_biggest_customers(transactions)-> str:
    header = "# Customers by total expenditure\n"
    r = process_biggest_customers(  transactions )
    return header + r
def process_biggest_customers(df) -> str :
    # Group by customer ID and calculate total sales
    grouped = df.groupby("Customer_ID", as_index=False).agg(
        Total_Sales=("Sales_Amount", "sum")
    )

    # Sort by total sales in descending order
    sorted_grouped = grouped.sort_values(by="Total_Sales", ascending=False)

    # Format the results into a string
    result = f"# number of customers = {len(sorted_grouped)}\n"
    for _, row in sorted_grouped.iterrows():
        result += f"| ID_{row['Customer_ID']} | £{row['Total_Sales']:.2f} |\n"

    return result + "-----------------"


    #-------------------------------------------------------------------------------------------------------------------

def main_things_to_profile( transactions ):
    """
    Main function to process the scanner_data.csv file and display the transactions.
    """
    print(f"\nTotal Transactions Processed: {len(transactions)}\n")
    print("Doing product report ( 10 seconds ) ")
    df = create_transactions_dataframe(transactions)
    with Profile() as profile:
        prod_report = report_best_selling_products(df)  # string
        print("doing sales report 1 seconds ")
        daily_sales = report_daily_sales(df)  # string
        print("doing customer report ( 200 seconds) ")
        customers = report_biggest_customers(df)  # string

    info = Stats(profile).strip_dirs().sort_stats(SortKey.CUMULATIVE)
    print("---------PROFILING RESULTS---------")
    info.print_stats()
    return prod_report, daily_sales, customers


if __name__ == "__main__":
    file_path = 'scanner_data.csv'  # Ensure this path is correct
    transactions = process_scanner_data_DO_NOT_PROFILE(file_path)

    # this is the stuff to profile
    prod_report, daily_sales, customers =  main_things_to_profile(transactions)



    # DON'T PROFILE the code below -
    with open("prod_report.csv", "w") as file:
        file.write(prod_report)

    with open("daily_sales.csv", "w") as file:
        file.write(daily_sales)

    with open("best_customers.csv", "w") as file:
        file.write(customers)

    print("please check prod_report.csv is the same result as prod_report_CORRECT.csv ")
    print("please check daily_sales.csv is the same result as daily_sales_CORRECT.csv ")
    print("please check best_customers.csv is the same result as best_customers_CORRECT.csv ")

