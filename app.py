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
    urgency: str
    is_done: bool

# Create Streamlit app
def main():
    st.title(" GHEA's TO DO LIST TRACKER")
    
    # Create a connection to the database
    conn = sqlite3.connect('task_tracker.sqlite3')
    cursor = conn.cursor()  # enable us to run SQL commands

    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks( created_at DATETIME DEFAULT CURRENT_TIMESTAMP, created_by TEXT, category TEXT, task_name TEXT, description TEXT, urgency TEXT, is_done BOOLEAN)''')
    #cursor.execute('''INSERT INTO tasks VALUES('2021-10-10 10:00:00', 'Ghea', 'Side Project', 'Send email', 'Send email to doctor', 'high', 0)''')


    conn.commit()

    # Display sample values from task table
    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall()
    
    # Create an HTML table to display tasks with checkboxes
    table_html = "<table><tr><th>Created At</th><th>Created By</th><th>Category</th><th>Task Name</th><th>Description</th><th>Urgency</th><th>Is Done</th></tr>"
    for row in rows:
        created_at, created_by, category, task_name, description, urgency, is_done = row
        checkbox = f'<input type="checkbox" {("checked" if is_done else "")} disabled>'
        table_html += f"<tr><td>{created_at}</td><td>{created_by}</td><td>{category}</td><td>{task_name}</td><td>{description}</td><td>{urgency}</td><td>{checkbox}</td></tr>"
    table_html += "</table>"
    
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Create a form to add a new task
    st.subheader('Add a New Task:')
    created_at = st.text_input('Created at')
    created_by = st.text_input('Created by')
    
    category_options = ['School', 'Personal', 'Side Project', 'Others']
    category = st.selectbox('Category', category_options)
    
    task_name = st.text_input('Task name')
    description = st.text_input('Description')
    
    urgency_options = ['High', 'Medium', 'Low']
    urgency = st.selectbox('Urgency', urgency_options)
    
    is_done = st.checkbox('Is done?')
    
    if st.button("Submit"):
        new_task = TaskSettings(created_at=datetime.datetime.now(), created_by=created_by, category=category, task_name=task_name, description=description, urgency=urgency, is_done=is_done)
        cursor.execute('INSERT INTO tasks VALUES(?, ?, ?, ?, ?, ?)', (new_task.created_at, new_task.created_by, new_task.category, new_task.task_name, new_task.description, new_task.urgency, new_task.is_done))
        conn.commit()
        st.write('New task added:', new_task)
    


 
if __name__ == "__main__":
    main()