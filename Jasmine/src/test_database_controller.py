#!"C:\Users\VSPan\AppData\Local\Programs\Python\Python37\python.exe"
print("Content-type: application/json")
print('')

# Add a new task
import sys, json
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../../test_database/') 
sys.path.insert(3, '../../cgi-bin/')
import test_database

request = json.load(sys.stdin)
# The string below - for debugging purposes
# request = {"userAction":"nuke_test_base",
# "databaseName":"../../test_database/test_database.db"}
type_of_action = request.get('userAction')
database_name = request.get('databaseName')
if type_of_action == 'create_test_base':
    test_database.common_setUp(test_database=database_name)
if type_of_action == 'nuke_test_base':
    test_database.common_tearDown(test_database=database_name)
