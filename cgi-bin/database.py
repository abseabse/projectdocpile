#!"C:\Users\VSPan\AppData\Local\Programs\Python\Python37\python.exe"
# Module to manipulate database


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
        Done            integer,
        Default_status  integer
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

def add_task(database_name=database_name, task_name=None, 
             task_status=None, parent_task=None):
    # Adds a new task in the database
    # if task status is not given defines the default status instead
    if not task_status:
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute('''pragma foreign_keys = on''')
        c.execute('''SELECT Task_status_ID FROM task_statuses 
                     WHERE Default_status = 1 LIMIT 1''')
        task_status = c.fetchone()[0]
        conn.commit()
        conn.close()
    conn = sqlite3.connect(database_name)
    c = conn.cursor()   
    c.execute('''INSERT INTO Tasks VALUES (null, ?, ?, ?)''',
            (task_name, task_status, parent_task)) 
    # Returns the ID of the new task
    c.execute('''pragma foreign_keys = on''')
    c.execute('''SELECT max(Task_ID) FROM Tasks''')
    added_task_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    return {"task_id": added_task_id}

def get_task(task_ID, database_name=database_name):
    # gets task information
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''pragma foreign_keys = on''')
    c.execute('''SELECT * FROM Tasks WHERE Task_ID = ?''', (task_ID,))
    task = c.fetchone()
    conn.commit()
    conn.close()
    if task:
        task_as_a_dictionary = {}
        task_as_a_dictionary['task_id'] = task[0]
        task_as_a_dictionary['task_name'] = task[1]
        task_as_a_dictionary['task_status'] = task[2]
        task_as_a_dictionary['task_parent'] = task[3]
        return task_as_a_dictionary
    else:
        return None

def get_doc(doc_ID, database_name=database_name):
    # gets doc information
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''pragma foreign_keys = on''')
    c.execute('''SELECT * FROM Docs WHERE Doc_ID = ?''', (doc_ID,))
    doc = c.fetchone()
    conn.close()
    if doc:
        doc_as_a_dictionary = {}
        doc_as_a_dictionary['doc_id'] = str(doc[0])
        doc_as_a_dictionary['doc_name'] = doc[1]
        doc_as_a_dictionary['doc_link'] = doc[2]
        return doc_as_a_dictionary
    else:
        return None

def delete_task_docs(task_id, database_name=database_name):
    # Deletes all the docs, attached to the task
    # FIXME write the function
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    # Gets the list of docs attached to the task given
    c.execute('''pragma foreign_keys = on''')
    c.execute('''SELECT Docs.Doc_ID From Tasks_docs JOIN Docs 
                    ON Tasks_docs.Doc_ID = Docs.Doc_ID 
                    WHERE Tasks_docs.Task_ID = ?''', (task_id,))
    docs_to_delete = c.fetchall()
    # Deletes these docs
    for doc in docs_to_delete:
        c.execute('''DELETE FROM Tasks_docs WHERE Tasks_docs.Doc_ID = ?''', doc)
        c.execute('''DELETE FROM Docs WHERE Docs.Doc_ID = ?''', doc)
    conn.commit()
    conn.close()
    
def delete_task(task_id, database_name=database_name):
    # Deletes a task
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''pragma foreign_keys = on''')
    c.execute('''DELETE from Tasks WHERE Task_ID = ?''', (task_id,))
    conn.commit()
    conn.close()

def update_task(task_id, task_info, database_name=database_name):
    # Updates an existing task. task_update should be a tuple
    # in this form: (new_task_name, new_task_status, new_parent_task)
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''pragma foreign_keys = on''')
    if 'task_name' in task_info:
        c.execute('''UPDATE Tasks SET Task = ? 
                     WHERE Task_ID = ?''', 
                     (task_info['task_name'], task_id))
    if 'task_status' in task_info:
        c.execute('''UPDATE Tasks SET Task_status = ? 
                     WHERE Task_ID = ?''',
                     (task_info['task_status'], task_id))
    if 'task_parent' in task_info:
        c.execute('''UPDATE Tasks SET Parent_task = ? 
                     WHERE Task_ID = ?''',
                     (task_info['task_parent'], task_id))
    conn.commit()
    conn.close()

def add_doc(doc_info, database_name=database_name):
    # Adds a new document.
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''pragma foreign_keys = on''')
    if 'doc_link' in doc_info:
        c.execute('''INSERT INTO Docs VALUES (null, ?, ?)''', 
                  (doc_info['doc_name'], doc_info['doc_link']))
    else:
        c.execute('''INSERT INTO Docs VALUES (null, ?, ?)''', 
                  (doc_info['doc_name'], None))
    c.execute('''SELECT max(Doc_ID) FROM Docs''')
    added_doc_id = c.fetchone()[0]
    if doc_info['task_id'] is not None:
        c.execute('''INSERT INTO Tasks_docs VALUES (?, ?)''', 
                  (doc_info['task_id'], added_doc_id))
    conn.commit()
    conn.close()
    return {"doc_id": added_doc_id}

def delete_doc(doc_id, database_name=database_name):
    # Deletes an existing document with all the links
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''DELETE FROM Tasks_docs WHERE Doc_id = ?''', (doc_id,))
    c.execute('''DELETE FROM Docs WHERE Doc_ID = ?''', (doc_id,))
    conn.commit()
    conn.close()

def update_doc(doc_id, doc_update, database_name=database_name):
    # Updates an existing document. doc_update should be a tuple
    # in this form: (new_name, new_link, new_task_id)
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    if 'doc_name' in doc_update:
        c.execute('''UPDATE Docs SET Doc = ?
                     WHERE Doc_ID = ?''',
                     (doc_update['doc_name'], doc_id))
    if 'doc_link' in doc_update:
        c.execute('''UPDATE Docs SET Doc_link = ?
                     WHERE Doc_ID = ?''',
                     (doc_update['doc_link'], doc_id))
    if 'doc_task' in doc_update:
        c.execute('''UPDATE Tasks_docs SET Task_ID = ?
                     WHERE Doc_ID = ?''',
                     (doc_update['doc_task'], doc_id))
    conn.commit()
    conn.close()

def add_task_status(database_name, status, is_done, is_default=0):
    # Adds a new task status
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''INSERT INTO Task_statuses VALUES (null, ?, ?, ?)''', 
              (status, is_done, is_default))
    conn.commit()
    conn.close()

def get_task_tuple(database_name=database_name):
    # Gets list of all tasks
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''SELECT * FROM Tasks''')
    raw_task_list = c.fetchall()
    conn.commit()
    conn.close()
    list_of_tasks = []
    for item in raw_task_list:
        item_to_add = {}
        item_to_add["task_id"] = item[0]
        item_to_add["task_name"] = item[1]
        item_to_add["task_status"] = item[2]
        item_to_add["task_parent"] = item[3] if item[3] is not None else 0
        list_of_tasks.append(item_to_add)
    tuple_of_tasks = tuple(list_of_tasks)
    return tuple_of_tasks

def get_docs_tuple(database_name=database_name, task=None):
    # Gets list of all docs, connected to the task
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    if task:
        c.execute('''WITH RECURSIVE task_with_children(x) AS (
                            SELECT Task_ID FROM Tasks WHERE 
                                Tasks.Task_ID = ?
                            UNION ALL
                            SELECT Task_ID FROM Tasks, task_with_children WHERE 
					            Tasks.Parent_task = task_with_children.x LIMIT 1000
                            )
			            SELECT Docs.Doc_ID, Doc, Doc_link FROM 
                            (Docs JOIN Tasks_docs ON Docs.Doc_ID = Tasks_docs.Doc_ID) WHERE 
                                Tasks_docs.Task_ID in task_with_children''', (task,))
    else:
        c.execute('''SELECT * FROM Docs''')
    raw_docs_list = c.fetchall()
    conn.commit()
    conn.close()
    list_of_docs = []
    for item in raw_docs_list:
        item_to_add = {}
        item_to_add["doc_id"] = item[0]
        item_to_add["doc_name"] = item[1]
        list_of_docs.append(item_to_add)
    tuple_of_docs = tuple(list_of_docs)
    return tuple_of_docs

def get_task_info(task_id, database_name=database_name):
    # returns list of task properties. 
    # Output example: 
    # {"taskId": 44, "taskName": "new task", 
    #  "parentTaskId": 8, "parentTaskName": "newtask12345"}
    # TODO write the tests - see task 49
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''SELECT Tasks.Task_ID, 
                        Tasks.Task, 
                        Tasks.Parent_task, 
                        Parent_tasks.Task 
                 FROM Tasks LEFT JOIN Tasks AS Parent_tasks 
                 ON Tasks.Parent_task = Parent_tasks.Task_ID 
                 WHERE Tasks.Task_ID = ?''', (task_id,))
    raw_task_info = c.fetchone()
    conn.close()
    dictionary_task_info = {}
    dictionary_task_info["taskId"] = raw_task_info[0]
    dictionary_task_info["taskName"] = raw_task_info[1]
    dictionary_task_info["parentTaskId"] = raw_task_info[2]
    dictionary_task_info["parentTaskName"] = raw_task_info[3]
    return dictionary_task_info
