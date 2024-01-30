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

conn = sqlite3.connect('student.db')
cur = conn.cur() # enable us to run SQL commands
