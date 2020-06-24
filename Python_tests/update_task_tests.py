# Tests for update_task.py module
# Version: 1
# Date: 20.03.20
# Time: 0:26 GMT+5


# IMPORTS
import unittest
import sqlite3
import database
import update_task


# OPTIONS
test_database = 'test_database.db'
survey_mode = 1 # set to 1 not to nuke test_database after the last test

def common_setUp(self):
        if survey_mode == 1:
            database.nuke_database(test_database)
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
            'old',
            0,
            1
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
        test_c.execute('''INSERT INTO Docs VALUES (
            null,
            'test_doc.txt',
            'http://google.com'
        )''')
        test_c.execute('''INSERT INTO Tasks_docs VALUES (1, 1)''')
        test_conn.commit()
        test_conn.close()

def common_tearDown(self):
    if survey_mode == 1:
        pass
    else:
        database.nuke_database(test_database)


# TESTS
"""
class Test_get_task(unittest.TestCase):
    # Tests of update_task.Task.get_task
    
    def setUp(self):
        common_setUp(self)

    def tearDown(self):
        common_tearDown(self)

    def test_one(self):
        # Basic test for an existing task.
        # Shouldn't raise an error
        task = update_task.Task(1, test_database).get_task()
        self.assertEqual(task, {'task_id': 1, 'task_name': 'vopya', 'task_status': 1, 'task_parent': None})

    def test_two(self):
        # Test for a non-existing task.
        # Shouldn't raise an error
        task = update_task.Task(100, test_database).get_task()
        self.assertEqual(task, None)


class Test_update_task(unittest.TestCase):
    # Tests of update_task.Task.update_task

    def setUp(self):
        common_setUp(self)

    def tearDown(self):
        common_tearDown(self)

    def test_one(self):
        # Basic test.
        # Shouldn't raise an error
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''pragma foreign_keys = on''')
        test_c.execute('''SELECT * FROM Tasks WHERE Task_ID = 1''')
        task_before = test_c.fetchone()
        task = update_task.Task(1, test_database)
        task.update_task({'task_name': 'ronyaya kal', 'task_status': 1, 'task_parent': None})
        test_c.execute('''SELECT * FROM Tasks WHERE Task_ID = 1''')
        task_after = test_c.fetchone()
        test_c.close()
        self.assertEqual(task_before, (1, 'vopya', 1, None))
        self.assertEqual(task_after, (1, 'ronyaya kal', 1, None))


class Test_delete_task(unittest.TestCase):
    # Tests of update_task.Task.delete_task
    def setUp(self):
        common_setUp(self)

    def tearDown(self):
        common_tearDown(self)

    def test_one(self):
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''pragma foreign_keys = on''')
        test_c.execute('''SELECT * FROM Tasks WHERE Task_ID = 1''')
        task_before = test_c.fetchone()
        task = update_task.Task(1, test_database)
        task.delete_task()
        test_c.execute('''SELECT * FROM Tasks WHERE Task_ID = 1''')
        task_after = test_c.fetchone()
        test_c.close()
        self.assertEqual(task_before, (1, 'vopya', 1, None))
        self.assertEqual(task_after, None)


class Test_add_doc(unittest.TestCase):
    # Tests of update_task.Task.add_doc
    def setUp(self):
        common_setUp(self)

    def tearDown(self):
        common_tearDown(self)

    def test_one(self):
        # Basic test that adds a doc to an existing task.
        # Shouln't raise an error.
        test_conn = sqlite3.connect(test_database)
        test_c = test_conn.cursor()
        test_c.execute('''SELECT COUNT (*) FROM Docs''')
        number_of_docs_before = test_c.fetchone()[0]
        task = update_task.Task(1, test_database)
        task.add_doc({'doc_name': 'ololo iskal', 'doc_link': 'goga312.html'})
        test_c.execute('''SELECT COUNT (*) FROM Docs''')
        number_of_docs_after = test_c.fetchone()[0]
        test_c.close()
        self.assertEqual(number_of_docs_before, 0)
        self.assertEqual(number_of_docs_after, 1)
"""

class Test_get_doc(unittest.TestCase):
    # Tests of update_task.Doc.update_doc

    def setUp(self):
        common_setUp(self)

    def tearDown(self):
        common_tearDown(self)

    def test_one(self):
        doc_to_get = update_task.Doc(1, test_database)
        x = doc_to_get.get_doc()
        self.assertEqual(str(doc_to_get.doc_id), x["doc_id"])
        self.assertEqual('test_doc.txt', x["doc_name"])

# MAIN CYCLE
if __name__ == '__main__':
    unittest.main()