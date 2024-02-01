import sqlite3
import streamlit as st
from pydantic_settings import BaseSettings
import datetime
import pandas as pd

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
    
    st.subheader('Existing Tasks:')
    df = pd.DataFrame(rows, columns=['created_at', 'created_by', 'category', 'task_name', 'description', 'is_done'])
    st.write(df)
    
    # Create a form to add a new task
    st.subheader('Add a New Task:')
    created_by = st.text_input('Created by')
    
    category_options = ['School', 'Personal', 'Side Project', 'Others']
    category = st.selectbox('Category', category_options)
    task_name = st.text_input('Task name')
    description = st.text_input('Description')
    is_done = st.checkbox('Is done?')
    
    if st.button("Submit"):
        new_task = TaskSettings(created_at=datetime.datetime.now(), created_by=created_by, category=category, task_name=task_name, description=description, is_done=is_done)
        cursor.execute('INSERT INTO tasks VALUES(?, ?, ?, ?, ?, ?)', (new_task.created_at, new_task.created_by, new_task.category, new_task.task_name, new_task.description, new_task.is_done))
        conn.commit()
        st.write('New task added:', new_task)
    


 
if __name__ == "__main__":
    main()