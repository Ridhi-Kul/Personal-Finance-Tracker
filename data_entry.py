'''
OVERVIEW-
    1. Contains all functions related to getting information from user
    2. To main the main() declutered

KEYWORDS-
    1. prompt: ask user to input this before date. Done as we can be getting the date in multiple places for different reason
    2. allow_default: whether to have a default value of today's date
                      (used to have user hit enter and by default it will select today's date)

'''
from datetime import datetime
date_format = "%d-%m-%Y"
CATEGORIES = {"I":"Income", "E":"Expense"}

def get_date(prompt, allow_default = False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format) #Convert the date time object to a string using strftime()
    try:
        valid_date = datetime.strptime(date_str,date_format) #Validate the date by converting the string to a datetime object
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format")
        return get_date(prompt, allow_default) #Recursively calling the function till the time we do not get valid date
    

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <=0:
            raise ValueError("Amount must be non-negative non-zero value")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()

def get_category():
    category = input("Enter the category ('I' for INCOME or 'E' for EXPENSE): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    print("Invalid category. Please enter ('I' for INCOME or 'E' for EXPENSE): ")
    return get_category()

def get_description():
    return input("Enter a decription (OPTIONAL): ")