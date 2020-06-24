# Tests of database.py module
# Version: 5
# Date: 18.06.20
# Time: 22:40 GMT+5

# IMPORTS
import unittest
import sqlite3
import sys
# insert at 1, o is the script path (or '' in REPL)
sys.path.insert(1, '../cgi-bin/')
import database
sys.path.insert(2, '../test_database/')
import test_database as test_database_module

# OPTIONS
test_database = '../test_database/test_database.db'
survey_mode = 1 # set to 1 not to nuke test_database after the last test

def common_setUp(self):
        test_database_module.common_setUp(test_database)

def common_tearDown(self):
        test_database_module.common_tearDown(test_database)

# TEST BLOCK
"""
# TESTS OF DATABASE STRUCTURE
class Test_create_database(unittest.TestCase):
    # tests of database.create_database and database.nuke_database

    def setUp(self):
        if survey_mode == 1:
            database.nuke_database(test_database)

    def tearDown(self):
        database.nuke_database(test_database) 

    def test_one(self):
        # create base first time
        database.create_database(test_database)


class Test_create_database_table_tests(unittest.TestCase):
    # tests of tables structure
    
    def setUp(self):
        if survey_mode == 1:
            database.nuke_database(test_database)
        database.create_database(test_database)

    def tearDown(self):
        if survey_mode == 1:
            pass
        else:
            database.nuke_database(test_database)

    def test_one(self):
        # try to insert a value in table Task_statuses
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''pragma foreign_keys = on''')
        test_c.execute('''INSERT INTO Task_statuses VALUES (null, 'new', 0, 1)''')
        test_conn.commit()
        test_conn.close()

    def test_two(self):
        # try to insert a value in table Tasks.
        # Should give an error as the table has foreign keys constraints and we
        # haven't entered any values in according tables yet
        with self.assertRaises(sqlite3.IntegrityError):
            test_conn = sqlite3.connect(test_database)
            test_c = test_conn.cursor()
            test_c.execute('''pragma foreign_keys = on''') 
            test_c.execute('''INSERT INTO Tasks VALUES (
                null, 
                'drop feces',
                312,
                1
                )''')
            test_conn.commit()
            test_conn.close()

    def test_three(self):
        # try to insert a list of values in tables Tasks, Task_statuses.
        # Should not give an error, as all the foreign constraints are resolved
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''pragma foreign_keys = on''')
        test_c.execute('''INSERT INTO Task_statuses VALUES (null, 'new', 0, 1)''')
        test_c.execute('''INSERT INTO Tasks VALUES (
            null,
            'drop feces',
            1,
            null
            )''')
        test_c.execute('''INSERT INTO Tasks VALUES (
            null,
            'vopya',
            1,
            1
            )''')
        test_conn.commit()
        test_conn.close()

    def test_four(self):
        # try to insert a value in table Tasks_docs.
        # Should raise an error, as the foreign constraint is not met
        with self.assertRaises(sqlite3.IntegrityError):
            test_conn = sqlite3.connect(test_database)
            test_c = test_conn.cursor()
            test_c.execute('''pragma foreign_keys = on''')
            test_c.execute('''INSERT INTO Tasks_docs VALUES (1, 1)''')
            test_conn.commit()
            test_conn.close()

    def test_five(self):
        # try to insert an appropriate set of values in tables Task_statuses, 
        # Tasks, Docs, Task_docs.
        # Should not raise an error as all the foreign constraints met.
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''pragma foreign_keys = on''')
        test_c.execute('''INSERT INTO Task_statuses VALUES (null, 'new', 0, 1)''')
        test_c.execute('''INSERT INTO Tasks VALUES (
            null,
            'drop feces',
            1,
            null
            )''')
        test_c.execute('''INSERT INTO Docs VALUES (
            null,
            'vopya.html',
            'http://goga312.com/vopya.html'
            )''')
        test_c.execute('''INSERT INTO Tasks_docs VALUES (1, 1)''')
        test_conn.commit()
        test_conn.close()

    def test_six(self):
        # try to insert a value in table Tasks violating not null constraint.
        # Should raise an error.
        with self.assertRaises(sqlite3.IntegrityError):
            test_conn = sqlite3.connect(test_database)
            test_c = test_conn.cursor()
            test_c.execute('''pragma foreign_keys = on''')
            test_c.execute('''INSERT INTO Task_statuses VALUES (null, 'new', 0, 1)''')
            test_c.execute('''INSERT INTO Tasks VALUES (
                null,
                'drop feces',
                null,
                null
                )''')
            test_conn.commit()
            test_conn.close()

"""
# TESTS OF DATABASE.PY FUNCTIONS
class Test_add_task(unittest.TestCase):
    # tests of database.add_task

    def setUp(self):
        common_setUp(self)

    def tearDown(self):
        common_tearDown(self)

    def test_one(self):
        # Try to add a new task with no parent.
        # Should not raise an error.
        database.add_task(test_database, 'vopya', 1, None)

    def test_two(self):
        # Try to add a new task with a parent.
        # Should not raise an error.
        database.add_task(test_database, 'tupya', 1, 1)


class Test_delete_task(unittest.TestCase):
    # tests of database.delete_task

    def setUp(self):
        common_setUp(self)

    def tearDown(self):
        common_tearDown(self)

    def test_one(self):
        # try to delete an existing task without docs.
        # Shouldn't raise an error
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT COUNT(*) FROM Tasks''')
        number_of_tasks_before = test_c.fetchone()[0]
        test_conn.close()
        database.delete_task(3, test_database)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT COUNT(*) FROM Tasks''')
        number_of_tasks_after = test_c.fetchone()[0]
        self.assertEqual(number_of_tasks_before, number_of_tasks_after+1)
        test_conn.close()

    def test_two(self):
        # try to delete a non-existing task.
        # Shouldn't raise an error
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT COUNT(*) FROM Tasks''')
        number_of_tasks_before = test_c.fetchone()[0]
        test_conn.close()
        database.delete_task(312, test_database)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT COUNT(*) FROM Tasks''')
        number_of_tasks_after = test_c.fetchone()[0]
        self.assertEqual(number_of_tasks_before, number_of_tasks_after)
        test_conn.close()

    def test_three(self):
        # try to delete an existing task, task id is str (not int)
        # Shouldn't raise an error
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT COUNT(*) FROM Tasks''')
        number_of_tasks_before = test_c.fetchone()[0]
        test_conn.close()
        database.delete_task("3", test_database)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT COUNT(*) FROM Tasks''')
        number_of_tasks_after = test_c.fetchone()[0]
        self.assertEqual(number_of_tasks_before, number_of_tasks_after+1)
        test_conn.close()

    def test_four(self):
        # try to delete a task with docs attached.
        # Should raise an error
        with self.assertRaises(sqlite3.IntegrityError):
            database.delete_task(1, test_database)


class Test_delete_task_docs(unittest.TestCase):
    # Tests of function database.delete_task_docs

    def setUp(self):
        common_setUp(self)

    def tearDown(self):
        common_tearDown(self)

    def test_one(self):
        # basic test to delete task docs for an existing task
        # Shouldn't raise an error
        task_to_delete_docs = 2
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''pragma foreign_keys = on''')
        test_c.execute('''SELECT COUNT(*) FROM Docs''')
        number_of_docs_before = test_c.fetchone()[0]
        test_conn.close()
        database.delete_task_docs(task_to_delete_docs, test_database)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()        
        test_c.execute('''pragma foreign_keys = on''')
        test_c.execute('''SELECT COUNT(*) FROM Docs''')
        number_of_docs_after = test_c.fetchone()[0]
        test_conn.close()
        self.assertEqual(number_of_docs_before, 3)
        self.assertEqual(number_of_docs_after, 1)

    def test_two(self):
        # basic test to delete task docs for a non-existing task.
        # Shouldn't raise an error
        task_to_delete_docs = 312
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''pragma foreign_keys = on''')
        test_c.execute('''SELECT COUNT(*) FROM Docs''')
        number_of_docs_before = test_c.fetchone()[0]
        test_conn.close()
        database.delete_task_docs(task_to_delete_docs, test_database)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()        
        test_c.execute('''pragma foreign_keys = on''')
        test_c.execute('''SELECT COUNT(*) FROM Docs''')
        number_of_docs_after = test_c.fetchone()[0]
        test_conn.close()
        self.assertEqual(number_of_docs_before, 3)
        self.assertEqual(number_of_docs_after, 3)


class Test_get_doc(unittest.TestCase):
    # Tests of function database.get_doc

    def setUp(self):
        common_setUp(self)

    def tearDown(self):
        common_tearDown(self)

    def test_one(self):
        # Basic test of an existing doc.
        # Shouldn't raise an error.
        first_doc = database.get_doc(1, test_database)
        self.assertEqual({'doc_id': '1', 'doc_name': 'vopya.doc', 
                          'doc_link': 'https://vopya.com'}, first_doc)

    def test_two(self):
        # Test of non-existing doc.
        # Shouldn't raise an error.
        imaginary_doc = database.get_doc(312, test_database)
        self.assertEqual(None, imaginary_doc)

   
class Test_update_task(unittest.TestCase):
    # Tests of database.update_task

    def setUp(self):
        common_setUp(self)

    def tearDown(self):
        common_tearDown(self)

    def test_one(self):
        # Try to change all task attributes: name, status and parent.
        # Shouldn't raise an error
        task_to_update = 2
        updating_record = {'task_name': 'drop feces', 
                           'task_status': 2, 'task_parent': 1}
        database.update_task(task_to_update, updating_record, test_database)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT * FROM Tasks WHERE Task_ID = ?''', 
                       (task_to_update,)
                      )
        updated_record = test_c.fetchone()
        test_conn.close()
        self.assertEqual(updated_record[0], task_to_update)                     
                         # task id
        self.assertEqual(updated_record[1], updating_record['task_name'])       
                         # task name
        self.assertEqual(updated_record[2], updating_record['task_status'])     
                         # task status
        self.assertEqual(updated_record[3], updating_record['task_parent'])     
                         # parent task

    def test_two(self):
        # try to change only one task attribute: status.
        # Shouldn't raise an error
        task_to_update = 2
        updating_record = {
            # 'task_name': None, 
            'task_status': 2
            # 'task_parent': None
            }
        database.update_task(task_to_update, updating_record, test_database)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT * FROM Tasks WHERE Task_ID = ?''', 
                       (task_to_update,)
                      )
        updated_record = test_c.fetchone()
        test_conn.close()
        self.assertEqual(updated_record[0], task_to_update)                     
                         # task id
        self.assertEqual(updated_record[1], 'tupya')                            
                         # task name
        self.assertEqual(updated_record[2], updating_record['task_status'])     
                         # task status
        self.assertEqual(updated_record[3], None)                               
                         # parent task


class Test_get_task(unittest.TestCase):
    # Tests of database.get_task

    def setUp(self):
        common_setUp(self)

    def tearDown(self):
        common_tearDown(self)

    def test_one(self):
        # test for existing task
        # Shouldn't raise an error
        task = database.get_task(1, test_database)
        self.assertEqual(task, {'task_name': 'vopya', 'task_id': 1, 
                                'task_status': 1, 'task_parent': None})

    def test_two(self):
        # test for non-existing task
        # Shouldn't raise an error
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT COUNT(*) FROM Tasks''')
        number_of_tasks = test_c.fetchone()[0]
        test_conn.close()
        task = database.get_task(number_of_tasks+1, test_database)
        self.assertEqual(task, None)


class Test_add_doc(unittest.TestCase):
    # Tests of database.add_doc

    def setUp(self):
        common_setUp(self)

    def tearDown(self):
        common_tearDown(self)

    def test_one(self):
        # try to add a new document in the base to a task.
        # Shouldn't raise an error.
        database.add_doc({'doc_name': 'drop_feces.txt', 
                          'doc_link': 'http://drop_feces.io',
                          'task_id': 1}, test_database)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT MAX(Doc_ID), Doc, Doc_link FROM Docs''')
        doc_added = test_c.fetchone()
        self.assertEqual('drop_feces.txt', doc_added[1])
        test_c.execute('''SELECT Task_ID, Max(Doc_ID) FROM Tasks_docs''')
        task_doc_link_added = test_c.fetchone()
        self.assertEqual(1, task_doc_link_added[0])
        self.assertEqual(4, task_doc_link_added[1])
        test_conn.close()

    def test_two(self):
        # try to add a new document in the base to a task, but without doc_link
        # Shouldn't raise an error.
        database.add_doc({'doc_name': 'drop_feces.txt',
                          'task_id': 1}, test_database)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT MAX(Doc_ID), Doc, Doc_link FROM Docs''')
        doc_added = test_c.fetchone()
        self.assertEqual('drop_feces.txt', doc_added[1])
        test_c.execute('''SELECT Task_ID, Max(Doc_ID) FROM Tasks_docs''')
        task_doc_link_added = test_c.fetchone()
        self.assertEqual(1, task_doc_link_added[0])
        self.assertEqual(4, task_doc_link_added[1])
        test_conn.close()

    def test_three(self):
        # try to add a new document without link to a task.
        # Shouldn't raise an error.
        database.add_doc({'doc_name': 'drop_feces.txt', 'task_id': None}, 
                          test_database)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT MAX(Doc_ID), Doc, Doc_link FROM Docs''')
        doc_added = test_c.fetchone()
        self.assertEqual('drop_feces.txt', doc_added[1])
        test_c.execute('''SELECT * FROM Tasks_docs WHERE Doc_ID = ?''', (doc_added[0],))
        task_doc_link_added = test_c.fetchone()
        self.assertEqual(type(None), type(task_doc_link_added))
        test_conn.close()


class Test_delete_doc(unittest.TestCase):
    # Tests of database.delete_doc

    def setUp(self):
        common_setUp(self)

    def tearDown(self):
        common_tearDown(self)

    def test_one(self):
        # Try to delete an existing document with a task link
        # Shouldn't raise an error.
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT COUNT(*) FROM Tasks_docs''')
        number_of_links_before = test_c.fetchone()[0]
        test_c.execute('''SELECT COUNT(*) FROM Docs''')
        number_of_docs_before = test_c.fetchone()[0]
        database.delete_doc(test_database, 1)
        test_c.execute('''SELECT COUNT(*) FROM Tasks_docs''')
        number_of_links_after = test_c.fetchone()[0]
        self.assertEqual(number_of_links_after, int(number_of_links_before)-1)
        test_c.execute('''SELECT COUNT(*) FROM Docs''')
        number_of_docs_after = test_c.fetchone()[0]
        self.assertEqual(number_of_docs_after, int(number_of_docs_before)-1)
        test_conn.close()
      

class Test_update_doc(unittest.TestCase):
    # Tests of database.update_doc

    def setUp(self):
        common_setUp(self)

    def tearDown(self):
        common_tearDown(self)

    def test_one(self):
        # Try to update an existing task changing all its attributes.
        # Shouldn't raise an error
        doc_update = {'doc_name': 'ronyal_iskal.txt', 
                      'doc_link': 'http://search-feces.info', 'doc_task': 2}
        database.update_doc(1, doc_update, test_database)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT * FROM Docs WHERE Doc_ID = ?''', (1,))
        updated_row = test_c.fetchone()
        self.assertEqual(updated_row[0], 1)
        self.assertEqual(updated_row[1], 'ronyal_iskal.txt')
        self.assertEqual(updated_row[2], 'http://search-feces.info')
        test_c.execute('''SELECT * FROM Tasks_docs WHERE Doc_ID = ?''', (1,))
        updated_link = test_c.fetchone()
        self.assertEqual(doc_update['doc_task'], updated_link[0])
        test_conn.close()

    def test_two(self):
        # Try to update an existing task changing only one attribute.
        # Shouldn't raise an error
        doc_update = {'doc_name': None, 'doc_link': 'c:/feces/drop.txt', 
                      'doc_task': 1}
        database.update_doc(1, doc_update, test_database)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT * FROM Docs WHERE Doc_ID = ?''', (1,))
        updated_row = test_c.fetchone()
        self.assertEqual(updated_row[0], 1)
        self.assertEqual(updated_row[1], doc_update['doc_name'])
        self.assertEqual(updated_row[2], 'c:/feces/drop.txt')
        test_c.execute('''SELECT * FROM Tasks_docs WHERE Doc_ID = ?''', (1,))
        updated_link = test_c.fetchone()
        self.assertEqual(1, updated_link[0])
        test_conn.close()


class Test_add_task_status(unittest.TestCase):
    # Tests of database.add_task_status
    
    def setUp(self):
        common_setUp(self)

    def tearDown(self):
        common_tearDown(self)

    def test_one(self):
        # Try to add a new status.
        # Shouldn't raise an error.
        database.add_task_status(test_database, 'new', 0, 1)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT MAX(Task_status_ID), 
                                 Task_status, 
                                 Done, 
                                 Default_status 
                          FROM Task_statuses''')
        added_status = test_c.fetchone()
        added_status_id = added_status[0]
        test_c.close()
        self.assertEqual(added_status, (added_status_id, 'new', 0, 1))


class Test_get_tasks_tuple(unittest.TestCase):
    # Tests of database.get_tasks_tuple
   
    def setUp(self):
        common_setUp(self)

    def tearDown(self):
        common_tearDown(self)
    
    def test_one(self):
        # Try to get the list of all the tasks in the base.
        # Shouldn't raise an error.
        added_tasks = database.get_task_tuple(test_database)
        self.assertEqual(added_tasks, ({"task_id": 1, 
                                        "task_name": "vopya", 
                                        "task_status": 1, 
                                        "task_parent": 0
                                       }, 
                                       {"task_id": 2, 
                                        "task_name": "tupya", 
                                        "task_status": 1, 
                                        "task_parent": 0
                                       },
                                       {"task_id": 3, 
                                        "task_name": "tupya", 
                                        "task_status": 1, 
                                        "task_parent": 0
                                       }
                                      )
                        )

    def test_two(self):
        # Try to use a relative path to the database location.
        # Shouldn't raise an error.
        added_tasks = database.get_task_tuple(
                "../test_database/test_database.db"
                )
        with self.assertRaises(AssertionError):
            self.assertEqual(added_tasks, 312)


class Test_get_docs_tuple(unittest.TestCase):
    # Tests of database.get_docs_tuple

    def setUp(self):
        common_setUp(self)

    def tearDown(self):
        common_tearDown(self)

    def test_one(self):
        # A simple test of return form without task given.
        # Shouldn't raise an error.
        added_docs = database.get_docs_tuple(test_database)
        self.assertEqual(added_docs, ({"doc_id": 1, "doc_name": "vopya.doc"}, 
                                      {"doc_id": 2, "doc_name": "tupya.xls"},
                                      {"doc_id": 3, "doc_name": "mnogo.txt"}))

    def test_two(self):
        # More complicated test, with the task given. There are docs connected
        # with the task. Shouldn't raise an error.
        test_task = 2
        # 2 is the number of the task with docs (see setUp function)
        docs = database.get_docs_tuple(test_database, test_task)
        self.assertEqual(docs, ({"doc_id": 1, "doc_name": "vopya.doc"},
                                {"doc_id": 3, "doc_name": "mnogo.txt"}))

    def test_three(self):
        # Test when there is no docs connected with the task.
        # Shouldn't raise an error.
        test_task = 4
        # 4 is the number of nonexisting task (see setUp function)
        pass
        docs = database.get_docs_tuple(test_database, test_task)
        self.assertEqual(docs, ())

    def test_four(self):
        # Test when there is an inappropriate input to a function: str instead
        # of int. Shouldn't raise an error
        test_task = "2"
        # 2 is the number of the task with docs (see setUp function) 
        # converted to str 
        docs = database.get_docs_tuple(test_database, test_task)
        self.assertEqual(docs, ({"doc_id": 1, "doc_name": "vopya.doc"},
                                {"doc_id": 3, "doc_name": "mnogo.txt"}))


# MAIN CYCLE
if __name__ == '__main__':
    unittest.TestLoader.sortTestMethodsUsing = None
    unittest.main()
