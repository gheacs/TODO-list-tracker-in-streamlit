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
    urgency: str
    is_done: bool

# Create Streamlit app
def main():
    st.title("GHEA's TO DO LIST TRACKER")

    # Create a connection to the database
    conn = sqlite3.connect('task_tracker.sqlite3')
    cursor = conn.cursor()  # Enable us to run SQL commands

    # Initialize the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks(
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT,
            category TEXT,
            task_name TEXT,
            description TEXT,
            urgency TEXT,
            is_done BOOLEAN
        )
    ''')
    conn.commit()

    # Retrieve tasks from the database
    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall()

    # Sidebar for task filtering
    st.sidebar.subheader('Filter Tasks:')
    category_filter = st.sidebar.selectbox('Filter by Category', ['All'] + list(set(row[2] for row in rows)))
    urgency_filter = st.sidebar.selectbox('Filter by Urgency', ['All'] + list(set(row[5] for row in rows)))

    # Filter tasks based on sidebar selections
    filtered_rows = [row for row in rows if (category_filter == 'All' or row[2] == category_filter) and (urgency_filter == 'All' or row[5] == urgency_filter)]

    # Display tasks and handle removal
    for index, row in enumerate(filtered_rows):
        with st.container():
            cols = st.columns([1, 1, 1, 1, 1, 1, 1, 0.5])
            created_at, created_by, category, task_name, description, urgency, is_done = row
            cols[0].write(created_at)
            cols[1].write(created_by)
            cols[2].write(category)
            cols[3].write(task_name)
            cols[4].write(description)
            cols[5].write(urgency)

            # Generate unique keys using the row index
            checkbox_key = f"{created_at}_{task_name}_{index}"
            remove_button_key = f"remove_{created_at}_{index}"

            cols[6].checkbox("Done", is_done, disabled=True, key=checkbox_key)
            if cols[7].button("Remove", key=remove_button_key):
                cursor.execute("DELETE FROM tasks WHERE created_at = ?", (created_at,))
                conn.commit()
                st.experimental_rerun()

    # Form to add a new task
    st.subheader('Add a New Task:')
    created_at = st.date_input('Created at', value=datetime.datetime.now())
    created_by = st.text_input('Created by')
    category_options = ['School', 'Personal', 'Side Project', 'Others']
    category = st.selectbox('Category', category_options)
    task_name = st.text_input('Task name')
    description = st.text_input('Description')
    urgency_options = ['High', 'Medium', 'Low']
    urgency = st.selectbox('Urgency', urgency_options)
    is_done = st.checkbox('Is done?', key='is_done_new_task')

    if st.button("Submit"):
        new_task = TaskSettings(
            created_at=created_at,
            created_by=created_by,
            category=category,
            task_name=task_name,
            description=description,
            urgency=urgency,
            is_done=is_done
        )
        cursor.execute('INSERT INTO tasks VALUES(?, ?, ?, ?, ?, ?, ?)', (
            new_task.created_at, new_task.created_by, new_task.category,
            new_task.task_name, new_task.description, new_task.urgency, new_task.is_done
        ))
        conn.commit()
        st.write('New task added:', new_task)
        st.experimental_rerun()

if __name__ == "__main__":
    main()
