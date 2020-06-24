// Model module (business logic)
export async function getTaskList(databaseName=undefined) {
  let response = await fetch(
    'http://localhost/projectdocpile/cgi-bin/get_list_of_tasks.py', {
      method: 'POST',
      body: JSON.stringify({userAction: 'get_task_list', 
                            databaseName: databaseName})
      });    
  if (response.ok) {
    let json_response = await response.json();
    return json_response;
  } else {
      alert("HTTP-Error: " + response.status);
    }
}

export async function getDocList(taskId, databaseName=undefined) {
  let response = await fetch(
    'http://localhost/projectdocpile/cgi-bin/get_list_of_docs.py', {
      method: 'POST',
      body: JSON.stringify({userAction: 'get_doc_list',
                            taskId: taskId,
                            databaseName: databaseName})
      });    
  if (response.ok) {
    let json_response = await response.json();
    return json_response;
  } else {
      alert("HTTP-Error: " + response.status);
    }
}

export async function addTask(databaseName=undefined) {
  let response = await fetch(
    'http://localhost/projectdocpile/cgi-bin/add_a_task.py', {
        method: 'POST',
        body: JSON.stringify({userAction: 'add_a_task', 
                              taskName: 'new task', 
                              databaseName: databaseName})
        });
    if (response.ok) {
      let json_response = await response.json();
      return json_response.task_id;
    } else {
      alert("HTTP-Error: " + response.status);
    }
}

export async function addDoc(taskId, databaseName=undefined) {
  let docName = 'new doc';
  let response = await fetch(
    'http://localhost/projectdocpile/cgi-bin/update_task.py', {
      method: 'POST',
      body: JSON.stringify({userAction: 'add doc', 
                            docName: 'new doc', 
                            taskId: taskId,
                            databaseName: databaseName})
      });
  
  if (response.ok) {
      let addedDoc = await response.json();
      let addedDocId = addedDoc.doc_id;
      return JSON.stringify({docId: addedDocId,
                             docName: docName})
  } else {
    alert("Ошибка HTTP: " + response.status);
  }
}

export async function deleteDoc(docId, databaseName=undefined) {
  let response = await fetch(
    'http://localhost/projectdocpile/cgi-bin/update_task.py', {
      method: 'POST',
      body: JSON.stringify({userAction: 'delete doc', 
                            docId: docId,
                            databaseName: databaseName})
      });
  
  if (response.ok) {
      // pass
  } else {
    alert("Ошибка HTTP: " + response.status);
  }
}

