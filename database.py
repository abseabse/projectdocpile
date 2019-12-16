# Module to manipulate database
# Version: 3
# Date: 12.12.19
# Time: 22:40 GMT+5

# IMPORTS
import sqlite3

# OPTIONS
database_name= 'database.db'

# FUNCTIONS
def create_database(database_name):
    # Creates a base of a predesigned structure
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''pragma foreign_keys = on''')
    c.execute('''CREATE TABLE Task_statuses (
        Task_status_ID  INTEGER PRIMARY KEY,
        Task_status     text,
        Done            integer
        )''')
    c.execute('''CREATE TABLE Tasks (
        Task_ID     INTEGER PRIMARY KEY,
        Task        text,
        Task_status integer NOT NULL,
        Parent_task integer,
        FOREIGN KEY (Task_status) REFERENCES Task_statuses(Task_status_ID),
        FOREIGN KEY (Parent_task) REFERENCES Tasks(Task_ID)
        )''')
    c.execute('''CREATE TABLE Docs (
        Doc_ID      INTEGER PRIMARY KEY,
        Doc         text,
        Doc_link    text
        )''')
    c.execute('''CREATE TABLE Tasks_docs (
        Task_ID     integer NOT NULL,
        Doc_ID      INTEGER PRIMARY KEY,
        FOREIGN KEY (Task_ID) REFERENCES Tasks(Task_ID),
        FOREIGN KEY (Doc_ID) REFERENCES Docs(Doc_ID)
        )''')
    conn.commit()
    conn.close()

def nuke_database(database_name):
    # Wipes off the created base
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS Tasks_docs''')
    c.execute('''DROP TABLE IF EXISTS Docs''')
    c.execute('''DROP TABLE IF EXISTS Task_statuses''')
    c.execute('''DROP TABLE IF EXISTS Tasks''')
    conn.commit()
    conn.close()

def add_task(database_name, task_name, task_status, parent_task='null'):
    # Adds a new task in the database
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''pragma foreign_keys = on''')
    c.execute('''INSERT INTO Tasks VALUES (null, ?, ?, ?)''',
            (task_name, task_status, parent_task)) 
    conn.commit()
    conn.close()

def delete_task(database_name, task_ID):
    # Deletes a task
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''DELETE from Tasks WHERE Task_ID = ?''', (task_ID,))
    conn.commit()
    conn.close()

def update_task(database_name, task_ID, task_update):
    # Updates an existing task. task_update should be a tuple
    # in this form: (new_task, new_task_status, new_parent_task)
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    if task_update[0] is not None:
        c.execute('''UPDATE Tasks SET Task = ? 
                     WHERE Task_ID = ?''', 
                     (task_update[0], task_ID))
    if task_update[1] is not None:
        c.execute('''UPDATE Tasks SET Task_status = ? 
                     WHERE Task_ID = ?''',
                     (task_update[1], task_ID))
    if task_update[2] is not None:
        c.execute('''UPDATE Tasks SET Parent_task = ? 
                     WHERE Task_ID = ?''',
                     (task_update[2], task_ID))
    conn.commit()
    conn.close()

def add_doc(database_name, doc_name, doc_link, task_id):
    # Adds a new document.
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''INSERT INTO Docs VALUES (null, ?, ?)''', (doc_name, doc_link))
    c.execute('''SELECT max(Doc_ID) FROM Docs''')
    added_doc_id = c.fetchone()[0]
    c.execute('''INSERT INTO Tasks_docs VALUES (?, ?)''', (task_id, added_doc_id))
    conn.commit()
    conn.close()

def delete_doc(database_name, doc_id):
    # Deletes an existing document with all the links
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''DELETE FROM Tasks_docs WHERE Doc_id = ?''', (doc_id,))
    c.execute('''DELETE FROM Docs WHERE Doc_ID = ?''', (doc_id,))
    conn.commit()
    conn.close()

def update_doc(database_name, doc_id, doc_update):
    # Updates an existing document. doc_update should be a tuple
    # in this form: (new_name, new_link, new_task_id)
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    if doc_update[0] is not None:
        c.execute('''UPDATE Docs SET Doc = ?
                     WHERE Doc_ID = ?''',
                     (doc_update[0], doc_id))
    if doc_update[1] is not None:
        c.execute('''UPDATE Docs SET Doc_link = ?
                     WHERE Doc_ID = ?''',
                     (doc_update[1], doc_id))
    if doc_update[2] is not None:
        c.execute('''UPDATE Tasks_docs SET Task_ID = ?
                     WHERE Doc_ID = ?''',
                     (doc_update[2], doc_id))
    conn.commit()
    conn.close()