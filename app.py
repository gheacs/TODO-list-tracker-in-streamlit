# Importing the required libraries
import sqlite3
import streamlit as st
import pandas as pd

# Create Streamlit app

def main():
    st.title('Student Data')
    st.write('You can use this app to view the student data.')
    
if __name__ == "__main__":
    main()
   
# Create a connection to the database

conn = sqlite3.connect('student.sqlite3')
cursor = conn.cursor() # enable us to run SQL commands

cursor.execute('''CREATE TABLE IF NOT EXISTS student( student_numb INT, name TEXT, undergrad_program TEXT, undergrad_year INT, gpa REAL)''')