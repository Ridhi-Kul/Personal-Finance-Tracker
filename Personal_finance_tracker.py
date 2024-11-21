# IMPORTANT: TO ADD DATA TO FILE USE path + cls.CSV_FILE
# Here path has been used to create the csv file in a specific location as per desire
'''
OVERVIEW-
    1. Track and log your transactions
    2. Organize them
    3. Get summaries of income and expenses
    4. View data via graph

(*) BETTER THAN REGULAR USE APPS AS YOU CAN GET SUMMARIES OF DATA FROM THE MIDDLE OF THE MONTH AS WELL
    UNLIKE POPULAR APPS THAT ONLY SHOW A SUMMARY OF MONTHLY EXPENDITURE
(*) OPTIMISE BY ADDING A FEATURE TO SEE AVERAGE DAILY EXPENDITURE IN THAT PERIOD

MODULES USED- 
    1. MATPLOTLIB: Useful for plotting and seeing the graph
    2. PANDAS: Categorize and search for data within the CSV file

KEYWORDS-
    1. @classmethod: Has access to class but no access to instance. If not used before class methods, shows error since self not passed
    2. DataFrame: oblect within pandas that allows us to access different rows AND columns from a CSV file (2D data structure)
    3. to_csv(): EXPORT/SAVE data to csv file
    4. a or append: append data to the end of file instead of overwriting the existing data
    5. newline ="": avoids adding a newline after every record that we add to a csv file
    6. csvfile: file handler of our csv file made during the use of with open
    7. mask: something we can apply to different rows inside of DataFrame to see if we should select that row or not (in get_transactions)
    8. formatter: format any specific column. put in dictionary where 
                  {key: value} = {column_name: function applied to every single element in the column if we want to format it differently}
    9. D or Daily frequency: take filtered DataFrame with transactions and emsure we have row for every day and use sum() to aggregate data on the same day
    10. plt.figure(): setting up the screen / canvas

POINTS TO REMEMBER-
    .>  When we use "with open", there is no need to close and reopen the file in another mode inorder to switch between r,w,a
        Write all the functions to be performed in that segment within an indented block. As soon as all those lines of code finish, 
        python closes the file on its own
    .> filtered_df["date"] ---> picks the coluumn
    .> filtered_df[filtered_df["category"] == "Income"]["amount"] ---> picks amount from rows where column category = Income 
    .> .2f in format means rounding off to 2 decimal places (for things like amount)
    .> add() and plot_transaction() are written outside class CSV as 
        a) their work is to collect user data or plot and NOT manipulating the data from csv file
        b) involve user interaction or data visualization
'''

import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt

path = "Sem3_project/"

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date","amount","category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod 
    def initialize_csv(cls):
        try:
            pd.read_csv(path+cls.CSV_FILE) 
        except FileNotFoundError:
            df = pd.DataFrame(columns = cls.COLUMNS)
            df.to_csv(path + cls.CSV_FILE, index=False) # Index here refers to indexing the data in a csv file (0 to n-1)
    
    @classmethod
    def add_entry(cls,date,amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open (path + cls.CSV_FILE, "a", newline = "") as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames = cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added succcessfully. ")
    
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(path+cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format = CSV.FORMAT) # Access not just a row but all values in a column
        start_date = datetime.strptime(start_date,CSV.FORMAT) # Convert to datetime object from string
        end_date = datetime.strptime(end_date,CSV.FORMAT)
        mask = (df["date"] >= start_date) & (df["date"]<=end_date) # Bitwise and (used with pandas)
        filtered_df = df.loc[mask] # Locates and returns filtered DataFrame with only rows that satisfy mask
        if filtered_df.empty:
            print("No transactions found in the given data range. ")
        else:
            # Convert the dates back to string format. This is a header before we print info.
            print("-----------------------------------------------")
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print("-----------------------------------------------")

            # Prints without index and formats the datetime object to string
            print(filtered_df.to_string(index = False, formatters = {"date": lambda x: x.strftime(CSV.FORMAT)}))
            
            # Picks column category from filtered_df and selects those where it is Income. 
            # Then after selecting these columns,it selects these row, takes their amount and sum() them 
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSUMMARY:")
            print(f"Total Income: ₹{total_income: .2f}")
            print(f"Total Expense: ₹{total_expense: .2f}")
            effective = total_income - total_expense
            if effective >= 0:
                print(f"Net Savings: ₹{effective: .2f}")
            else:
                print(f"Net Savings: ₹{effective: .2f} or Over expense : ₹{-effective: .2f}")

            # Calculate the number of days
            num_days = (end_date - start_date).days + 1
            average_expenditure_per_day = total_expense / num_days
            print(f"Average / Per day expenditure from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)} ({num_days} days): ₹{average_expenditure_per_day: .2f}")

            return filtered_df


def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or press enter for today's date:", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    df.set_index('date',inplace = True) # Index is a way to locate and manipulate rows

    # Create 2 DataFrame as we need separate lines for income and expense on the graph
    # Also NEED to mark empty days as 0 to get a proper line, otherwise we will get separate lines for separate dates
    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value = 0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value = 0)
    plt.figure(figsize = (10,5)) # Height and width in inches
    plt.plot(income_df.index, income_df["amount"], label = "Income", color = "g") # .index here basically means the dates
    plt.plot(income_df.index, expense_df["amount"], label = "Expense", color = "r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and expenses over time")
    plt.legend() # Allows us to present 2 lines in 1 graph separated by colour
    plt.grid(True) # Enables grid lines
    plt.show()


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see the plot? (y/n): ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter again. ")

if __name__ == "__main__": #protecting the main. main can NOT be executed unless we directly execute this file 
    main()