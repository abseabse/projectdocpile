#!"C:\Users\VSPan\AppData\Local\Programs\Python\Python37\python.exe"
print("Content-type: application/json")
print('')

# Add a new task
import sys, json
import database

request = json.load(sys.stdin)
# The string below - for debugging purposes
# request = {"userAction":"get_task_list",
# "databaseName":"../test_database/test_database.db"}
type_of_action = request.get('userAction')
task_name = request.get('taskName')
database_name = request.get('databaseName')
if type_of_action == 'add_a_task':
    if database_name:
        added_task_id = database.add_task(task_name=task_name,
                                          database_name=database_name)
    else:
        added_task_id = database.add_task(task_name=task_name)
    f = json.dumps(added_task_id)
    print(f)
