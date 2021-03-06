# Module to create a test database
# Version: 2*
# Date: 10.06.20
# Time: 20:30 GMT+5

# IMPORTS
import sqlite3
import sys
import json
# insert at 1, o is the script path (or '' in REPL)
sys.path.insert(1, '../cgi-bin/')
sys.path.insert(2, '../test_database/')
import database

# OPTIONS
test_database = 'test_database.db'

# FUNCTIONS TO CREATE AND NUKE TEST DATABASE
def common_setUp(test_database):
    database.create_database(test_database)
    test_conn = sqlite3.connect(test_database)
    test_c = test_conn.cursor()
    test_c.execute('''pragma foreign_keys = on''')
    test_c.execute('''INSERT INTO Task_statuses VALUES (
        null,
        'new',
        0,
        1
        )''')
    test_c.execute('''INSERT INTO Task_statuses VALUES (
        null,
        'done',
        1,
        0
        )''')
    test_c.execute('''INSERT INTO Tasks VALUES (
        null,
        'vopya',
        1,
        null
        )''')
    test_c.execute('''INSERT INTO Tasks VALUES (
        null,
        'tupya',
        1,
        null
        )''')            
    test_c.execute('''INSERT INTO Tasks VALUES (
        null,
        'tupya',
        1,
        null
        )''') 
    test_c.execute('''INSERT INTO Docs VALUES (
        null, 
        'vopya.doc', 
        'https://vopya.com'
        )''')
    test_c.execute('''INSERT INTO Docs VALUES (
        null,
        'tupya.xls',
        'http://tupya.com'
        )''')
    test_c.execute('''INSERT INTO Docs VALUES (
        null,
        'mnogo.txt',
        'https://mnogo.com'
        )''')
    test_c.execute('''INSERT INTO Tasks_docs VALUES (2, 1)''')
    test_c.execute('''INSERT INTO Tasks_docs VALUES (1, 2)''')
    test_c.execute('''INSERT INTO Tasks_docs VALUES (2, 3)''')
    test_conn.commit()
    test_conn.close()

def common_tearDown(test_database):
    database.nuke_database(test_database)
