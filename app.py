import sqlite3
import streamlit as st
from pydantic_settings import BaseSettings
import datetime

# Define a pydantic settings model
class TaskSettings(BaseSettings):
    created_at: datetime.datetime
    created_by: str
    category: str
    task_name: str
    description: str
    is_done: bool

# Create Streamlit app
def main():
    st.title('TO DO LIST TRACKER')
    st.write('You can use this app to view the to-do list.')
    
    
    # Create a connection to the database
    conn = sqlite3.connect('task_tracker.sqlite3')
    cursor = conn.cursor()  # enable us to run SQL commands

    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks( created_at DATETIME DEFAULT CURRENT_TIMESTAMP, created_by TEXT, category TEXT, task_name TEXT, description TEXT, is_done BOOLEAN)''')
    cursor.execute('''INSERT INTO tasks VALUES('2021-10-10 10:00:00', 'Ghea', 'Side Project', 'Send email', 'Send email to doctor', 0)''')
    conn.commit()

    # Display sample values from task table
    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall()
    
    st.write('Sample values from task table:')
    for row in rows:
        st.write(row)



if __name__ == "__main__":
    main()