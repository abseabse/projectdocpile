# Tests for all python modules in the program
# Version: 3
# Date: 12.12.19
# Time: 22:40 GMT+5

# IMPORTS
import unittest
import sqlite3
import database

# OPTIONS
test_database = 'test_database.db'
survey_mode = 1 # set to 1 not to nuke test_database after the last test

# TEST BLOCK
# TESTS OF DATABASE STRUCTURE
class Test_create_database(unittest.TestCase):
    # tests for create_database() and nuke_database()

    def setUp(self):
        if survey_mode == 1:
            database.nuke_database(test_database)

    def tearDown(self):
        database.nuke_database(test_database) 

    def test_one(self):
        # create base first time
        database.create_database(test_database)


class Test_create_database_table_tests(unittest.TestCase):
    # tests for tables structure
    
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
        test_c.execute('''INSERT INTO Task_statuses VALUES (null, 'new', 0)''')
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
        test_c.execute('''INSERT INTO Task_statuses VALUES (null, 'new', 0)''')
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
        test_c.execute('''INSERT INTO Task_statuses VALUES (null, 'new', 0)''')
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
            test_c.execute('''INSERT INTO Task_statuses VALUES (null, 'new', 0)''')
            test_c.execute('''INSERT INTO Tasks VALUES (
                null,
                'drop feces',
                null,
                null
                )''')
            test_conn.commit()
            test_conn.close()

# TESTS OF DATABASE.PY FUNCTIONS
class Test_add_task(unittest.TestCase):
    # tests for database.add_task()

    def setUp(self):
        if survey_mode == 1:
            database.nuke_database(test_database)
        database.create_database(test_database)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''pragma foreign_keys = on''')
        test_c.execute('''INSERT INTO Task_statuses VALUES (
            null,
            'new',
            0
            )''')
        test_conn.commit()
        test_conn.close()

    def tearDown(self):
        if survey_mode == 1:
            pass
        else:
            database.nuke_database(test_database)

    def test_one(self):
        # Try to add a new task and then a second one, with the first as the parent
        # Should not raise an error.
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        database.add_task(test_database, 'vopya', 1, None)
        database.add_task(test_database, 'tupya', 1, 1)


class Test_delete_task(unittest.TestCase):
    # tests for database.delete_task()

    def setUp(self):
        if survey_mode == 1:
            database.nuke_database(test_database)
        database.create_database(test_database)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''pragma foreign_keys = on''')
        test_c.execute('''INSERT INTO Task_statuses VALUES (
            null,
            'new',
            0
            )''')
        test_c.execute('''INSERT INTO Tasks VALUES (
            null,
            'vopya',
            1,
            null
            )''')
        test_conn.commit()
        test_conn.close()

    def tearDown(self):
        if survey_mode == 1:
            pass
        else:
            database.nuke_database(test_database)

    def test_one(self):
        # try to delete an existing task.
        # Shouldn't raise an error
        database.delete_task(test_database, 1)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT max(Task_ID) FROM Tasks''')
        number_of_tasks = test_c.fetchone()[0]
        self.assertEqual(number_of_tasks, None)
        test_conn.commit()
        test_conn.close()

    def test_two(self):
        # try to delete a non-existing task.
        # Shouldn't raise an error
        database.delete_task(test_database, 312)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT max(Task_ID) FROM Tasks''')
        number_of_tasks = test_c.fetchone()[0]
        self.assertEqual(number_of_tasks, 1)
        test_conn.commit()
        test_conn.close()


class Test_update_task(unittest.TestCase):
    # Tests for database.update_task()

    def setUp(self):
        if survey_mode == 1:
            database.nuke_database(test_database)
        database.create_database(test_database)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''pragma foreign_keys = on''')
        test_c.execute('''INSERT INTO Task_statuses VALUES (
            null,
            'new',
            0
            )''')
        test_c.execute('''INSERT INTO Task_statuses VALUES (
            null,
            'old',
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
        test_conn.commit()
        test_conn.close()

    def tearDown(self):
        if survey_mode == 1:
            pass
        else:
            database.nuke_database(test_database)

    def test_one(self):
        # Try to change all task attributes: name, status and parent.
        # Shouldn't raise an error
        task_to_update = 2
        updating_record = ('drop feces', 2, 1)
        database.update_task(test_database, task_to_update, updating_record)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT * FROM Tasks WHERE Task_ID = ?''', (task_to_update,))
        updated_record = test_c.fetchone()
        test_conn.commit()
        test_conn.close()
        self.assertEqual(updated_record[0], task_to_update)      # task id
        self.assertEqual(updated_record[1], updating_record[0])  # task name
        self.assertEqual(updated_record[2], updating_record[1])  # task status
        self.assertEqual(updated_record[3], updating_record[2])  # parent task

    def test_two(self):
        # try to change only one task attribute: status.
        # Shouldn't raise an error
        task_to_update = 2
        updating_record = (None, 2, None)
        database.update_task(test_database, task_to_update, updating_record)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT * FROM Tasks WHERE Task_ID = ?''', (task_to_update,))
        updated_record = test_c.fetchone()
        test_conn.commit()
        test_conn.close()
        self.assertEqual(updated_record[0], task_to_update)     # task id
        self.assertEqual(updated_record[1], 'tupya')            # task name
        self.assertEqual(updated_record[2], updating_record[1]) # task status
        self.assertEqual(updated_record[3], None)               # parent task


class Test_add_doc(unittest.TestCase):
    # Tests for database.add_doc()

    def setUp(self):
        if survey_mode == 1:
            database.nuke_database(test_database)
        database.create_database(test_database)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''INSERT INTO Task_statuses VALUES (
            null,
            'new',
            0
            )''')
        test_c.execute('''INSERT INTO Tasks VALUES (
            null,
            'vopya',
            1,
            null
            )''')
        test_conn.commit()
        test_conn.close()
        
    def tearDown(self):
        if survey_mode == 1:
            pass
        else:
            database.nuke_database(test_database)

    def test_one(self):
        # try to add a new document in the base to a task.
        # Shouldn't raise an error.
        database.add_doc(test_database, 'drop_feces.txt', 'http://drop_feces.io', 1)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT * FROM Docs WHERE Doc_ID = ?''', (1,))
        doc_added = test_c.fetchone()
        self.assertEqual('drop_feces.txt', doc_added[1])
        test_c.execute('''SELECT * FROM Tasks_docs''')
        task_doc_link_added = test_c.fetchone()
        self.assertEqual(1, task_doc_link_added[0])
        self.assertEqual(1, task_doc_link_added[1])
        test_conn.commit()
        test_conn.close()


class Test_delete_doc(unittest.TestCase):
    # Tests for database.delete_doc()

    def setUp(self):
        if survey_mode == 1:
            database.nuke_database(test_database)
        database.create_database(test_database)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''INSERT INTO Task_statuses VALUES (
            null,
            'new',
            0
            )''')
        test_c.execute('''INSERT INTO Tasks VALUES (
            null,
            'vopya',
            1,
            null
            )''')
        test_c.execute('''INSERT INTO Docs VALUES (
            null,
            'drop_feces.txt',
            'http://vopya.html'
            )''')
        test_c.execute('''INSERT INTO Docs VALUES (
            null,
            'tupya.pdf',
            'c:/feces/tupya.pdf'
            )''')
        test_c.execute('''INSERT INTO Tasks_docs VALUES (1, 1)''')
        test_conn.commit()
        test_conn.close()
        
    def tearDown(self):
        if survey_mode == 1:
            pass
        else:
            database.nuke_database(test_database)

    def test_one(self):
        # Try to delete an existing document.
        # Shouldn't raise an error.
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT COUNT(*) FROM Tasks_docs''')
        number_of_links = test_c.fetchone()[0]
        self.assertEqual(number_of_links, 1)
        test_c.execute('''SELECT COUNT(*) FROM Docs''')
        number_of_docs = test_c.fetchone()[0]
        self.assertEqual(number_of_docs, 2)
        database.delete_doc(test_database, 1)
        test_c.execute('''SELECT COUNT(*) FROM Tasks_docs''')
        updated_number_of_links = test_c.fetchone()[0]
        self.assertEqual(updated_number_of_links, 0)
        test_c.execute('''SELECT COUNT(*) FROM Docs''')
        updated_number_of_docs = test_c.fetchone()[0]
        self.assertEqual(updated_number_of_docs, 1)
        test_conn.commit()
        test_conn.close()

class Test_update_doc(unittest.TestCase):
    # Tests for database.update_doc()

    def setUp(self):
        if survey_mode == 1:
            database.nuke_database(test_database)
        database.create_database(test_database)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''INSERT INTO Task_statuses VALUES (
            null,
            'new',
            0
            )''')
        test_c.execute('''INSERT INTO Tasks VALUES (
            null,
            'vopya',
            1,
            null
            )''')
        test_c.execute('''INSERT INTO Docs VALUES (
            null,
            'drop_feces.txt',
            'http://vopya.html'
            )''')
        test_c.execute('''INSERT INTO Docs VALUES (
            null,
            'tupya.pdf',
            'c:/feces/tupya.pdf'
            )''')
        test_c.execute('''INSERT INTO Tasks_docs VALUES (1, 1)''')
        test_conn.commit()
        test_conn.close()
        
    def tearDown(self):
        if survey_mode == 1:
            pass
        else:
            database.nuke_database(test_database)

    def test_one(self):
        # Try to update an existing task changing all its attributes.
        # Shouldn't raise an error
        doc_update = ('ronyal_iskal.txt', 'http://search-feces.info', 2)
        database.update_doc(test_database, 1, doc_update)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT * FROM Docs WHERE Doc_ID = ?''', (1,))
        updated_row = test_c.fetchone()
        self.assertEqual(updated_row[0], 1)
        self.assertEqual(updated_row[1], 'ronyal_iskal.txt')
        self.assertEqual(updated_row[2], 'http://search-feces.info')
        test_c.execute('''SELECT * FROM Tasks_docs WHERE Doc_ID = ?''', (1,))
        updated_link = test_c.fetchone()
        self.assertEqual(doc_update[2], updated_link[0])
        test_conn.commit()
        test_conn.close()

    def test_two(self):
        # Try to update an existing task changing only one attribute.
        # Shouldn't raise an error
        doc_update = (None, 'c:/feces/drop.txt', None)
        database.update_doc(test_database, 1, doc_update)
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT * FROM Docs WHERE Doc_ID = ?''', (1,))
        updated_row = test_c.fetchone()
        self.assertEqual(updated_row[0], 1)
        self.assertEqual(updated_row[1], 'drop_feces.txt')
        self.assertEqual(updated_row[2], doc_update[1])
        test_c.execute('''SELECT * FROM Tasks_docs WHERE Doc_ID = ?''', (1,))
        updated_link = test_c.fetchone()
        self.assertEqual(1, updated_link[0])
        test_conn.commit()
        test_conn.close()

# MAIN CYCLE
if __name__ == '__main__':
    unittest.main()
