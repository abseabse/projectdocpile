#!"C:\Users\VSPan\AppData\Local\Programs\Python\Python37\python.exe"
# print("Content-type: text/html")
print("Content-type: application/json")
print('')

# Get list of docs
import sys, json
import database

request = json.load(sys.stdin)
# The strings below - for debugging purposes
# request = {"userAction":"get_docs_list",
# "taskId":"1",
# "databaseName":"../test_database/test_database.db"}
type_of_action = request.get('userAction')
selected_task = request.get('taskId')
database_name = request.get('databaseName')
if type_of_action == 'get_doc_list':
    if database_name:
        docs_dictionary = database.get_docs_tuple(task=selected_task, 
                                                  database_name=database_name)
    else:
        docs_dictionary = database.get_docs_tuple(task=selected_task)
    f = json.dumps(docs_dictionary)
    print(f)
