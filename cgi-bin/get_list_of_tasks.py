#!"C:\Users\VSPan\AppData\Local\Programs\Python\Python37\python.exe"
# print("Content-type: text/html")
print("Content-type: application/json")
print('')

# Get list of tasks
import sys, json
import database

request = json.load(sys.stdin)
# The string below - for debugging purposes
# request = {"userAction":"get_task_list",
# "databaseName":"../test_database/test_database.db"}
type_of_action = request.get('userAction')
database_name = request.get('databaseName')
if type_of_action == 'get_task_list':
    if database_name:
        task_dictionary = database.get_task_tuple(database_name)
    else:
        task_dictionary = database.get_task_tuple()
    f = json.dumps(task_dictionary)
    print(f)
