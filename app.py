# Importing the required libraries
import sqlite3
import streamlit as st
import pandas as pd

# Create Streamlit app

def main():
    st.title('EXPENSE TRACKER')
    st.write('You can use this app to view the expense tracker.')
    
if __name__ == "__main__":
    main()
   
# Create a connection to the database

conn = sqlite3.connect('expense_tracker.sqlite3')
cursor = conn.cursor() # enable us to run SQL commands

cursor.execute('''CREATE TABLE IF NOT EXISTS expense( created_at DATETIME, created_by TEXT, expense_category TEXT, expense_name TEXT, expense_description TEXT, amount FLOAT, is_paid BOOLEAN)''')
cursor.execute('''INSERT INTO expense VALUES('2021-01-01', 'Ghea', 'Food', 'Lunch', 'Lunch at McDonalds', 10.00, 1)''')
conn.commit()
conn.close()

