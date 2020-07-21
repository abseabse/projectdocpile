#!"C:\Users\VSPan\AppData\Local\Programs\Python\Python37\python.exe"


# IMPORTS
import sys, json
import database

# OPTIONS
database_name = 'database.db'

# CODE
print("Content-type: application/json")
print('')

request = json.load(sys.stdin)
# TODO strings of code below - for debugging purposes
# request = {"userAction":"add doc","docName":"new doc"}
# request = {'userAction': 'modify task', 'taskId': '8', 'taskProperties': {'taskName': 'new task1334'}  
# request = {'userAction': 'modify task', 'taskId': '8', 'taskName': 'new task1234'}
# request = {"userAction":"modify task","taskId":"8","taskProperties":{"task_name":"new task1334"}} 
type_of_action = request.get('userAction')
doc_name = request.get('docName')
task_name = request.get('taskName')
task_info = request.get('taskProperties')
doc_id = request.get('docId')
task_id = request.get('taskId')
database_name = request.get('databaseName')
if type_of_action == 'modify task':
    # FIXME write the function
    f = open('log.txt', 'w')
    f.write('gogakal')
    f.close()    
    if database_name:
        database.update_task(task_id=task_id, 
                             task_info=task_info, 
                             database_name=database_name)
    else:
        database.update_task(task_id=task_id, 
                             task_info=task_info)
      

if type_of_action == 'delete task':
    if database_name:
        database.delete_task_docs(task_id=task_id,
                                  database_name=database_name)
        database.delete_task(task_id=task_id,
                             database_name=database_name)
    else:
        database.delete_task_docs(task_id=task_id)
        database.delete_task(task_id=task_id)
if type_of_action == 'add doc':
    if database_name:
        added_doc_id = database.add_doc(
            doc_info={'doc_name': doc_name, 'task_id': task_id}, 
            database_name=database_name)
    else:
        added_doc_id = database.add_doc(
            doc_info={'doc_name': doc_name, 'task_id': task_id})
    f = json.dumps(added_doc_id)
    print(f)
if type_of_action == 'delete doc':
    if database_name:
        database.delete_doc(doc_id, database_name=database_name)
    else:
        database.delete_doc(doc_id)
        

"""
if request['userAction'] == 'update task':
    task_to_update = Task(request["taskId"])
    task_to_update.update_task({'task_name': request['taskName']})
if request['userAction'] == 'add doc':
    task_to_add_doc = Task(request["taskId"])
    added_doc_id = task_to_add_doc.add_doc({'doc_name': request['docName']})
    print(type(added_doc_id))
    f = json.dumps(added_doc_id)
    print(f)
if request['userAction'] == 'update doc':
    doc_to_update = Doc(request['docId'])
    update = {}
    if 'docName' in request:
        update['doc_name'] = request['docName']
    if 'docLink' in request:
        update['doc_link'] = request['docLink']
    doc_to_update.update_doc(update)
if request['userAction'] == 'get doc':
    doc_to_return = Doc(request['docId'])
    doc_returned = doc_to_return.get_doc()
    f = json.dumps(doc_returned)
    print(f)
if request['userAction'] == 'delete task docs':
    task_to_delete_docs = Task(request["taskId"])
    task_to_delete_docs.delete_task_docs()
"""
