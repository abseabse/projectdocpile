// Presenter module

export function mainLoad() {
  let modal = document.getElementsByClassName('modal');
  let span = document.getElementsByClassName('close');
  for (let item of span) {
    item.onclick = function() {
      for (let item of modal) {
        item.style.display = "none";
      }
    };
  }
  window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
      event.target.style.display = "none";
    }
  };
}

export async function updateTasks(newTaskList, getDocList) {
  let taskList = await document.getElementById('tasks_list');
  // removes old tasks
  while (taskList.firstChild) {
    taskList.removeChild(taskList.firstChild);
  }
  // removes old docs
  let docsList = await document.getElementById('docs_list');
  while (docsList.firstChild) {
    docsList.removeChild(docsList.firstChild);
  }
  // adds actual tasks
  for (let item of newTaskList) {
    let node = await document.createElement('li');
    node.id = item.task_id;
    await node.classList.add("task");
    let text = await document.createTextNode(item.task_name);
    await node.appendChild(text);
    await taskList.appendChild(node);
    addEventsToTask(node, getDocList);
  }
  // adds actual docs
  let docList = await getDocList();
  updateDocs(docList);
}

export async function addEventsToTask(task, getDocList) {
  // adds selection to task
  task.onclick = async function() {
    await task.classList.toggle('selected');
    let newTaskList = await document.getElementsByClassName('task');
    for (let newTask of newTaskList) {
      if (newTask != task) {
        newTask.classList.remove('selected');
      }
    }
  // updates doc list
    if (task.classList.contains('selected')) {
      let docList = await getDocList(task.id);
      updateDocs(docList);
    } else {
      // assuming none of the task is currently selected 
      // displays full doc list
      let docList = await getDocList();
      updateDocs(docList);
    }
  };
  // opens task properties in a modal window
  task.ondblclick = function(event) {
    document.getElementById('modal_task_name').value = event.target.innerHTML;
    document.getElementById('modal_task_id').value = event.target.id;
    let modal = document.getElementById('task_window');
    modal.style.display = "block";
  };
}

export async function addEventsToDoc(doc) {
  // adds selection to doc
  doc.onclick = async function() {
    doc.classList.toggle('selected');
    let newDocList = document.getElementsByClassName('doc');
    for (let newDoc of newDocList) {
      if (newDoc != doc) {
        newDoc.classList.remove('selected');
      }
    }
  }
}

export function updateDocs(docs) {
  let docList = document.getElementById('docs_list');
  // remove old docs
  while (docList.firstChild) {
    docList.removeChild(docList.firstChild);
  }
  // add actual docs
  for (let item of docs) {
    let node = document.createElement('li');
    node.id = item.doc_id;
    node.classList.add("doc");
    let text = document.createTextNode(item.doc_name);
    node.appendChild(text);
    docList.appendChild(node);
    addEventsToDoc(node);
  }
}

export function addTask(taskAdded, getDocList) {
  let taskList = document.getElementById('tasks_list');
  let node = document.createElement('li');
  node.id = taskAdded;
  node.classList.add("task");
  let text = document.createTextNode("new task");
  node.appendChild(text);
  taskList.appendChild(node);
  addEventsToTask(node, getDocList);
}

export function addDoc(docAdded) {
  let docList = document.getElementById('docs_list');
  let node = document.createElement('li');
  node.id = docAdded.docId;
  node.classList.add("doc");
  let text = document.createTextNode("new doc");
  node.appendChild(text);
  docList.appendChild(node);
  addEventsToDoc(node);
}

export async function deleteTask(taskId, getDocList) {
  // closes the modal task window
  let taskWindow = await document.getElementById('task_window');
  taskWindow.style.display = "none";
  // removes the task from UI
  let allTheTasksInUI = await document.querySelectorAll('.task');
  for (let item of allTheTasksInUI) {
    if (item.id == taskId) {
      item.remove();
    }
  }
  // shows all the docs in base (as no tasks is currently selected)
  let docList = await getDocList();
  updateDocs(docList);
}

export function getSelectedTask() {
  let taskSelected = document.querySelector('.task.selected');
  return taskSelected;
}

// write the function
export function getDocSelected() {
  // returns the currently selected doc id
  let docSelected = document.querySelector('.doc.selected');
  if (docSelected) {
    return docSelected.id;
  } else {
    return null;
  }
}

export function deleteDoc(docId) {
  // deletes a doc
  for (let node of document.getElementById('docs_list').childNodes) {
    if (node.id == docId) {
      node.remove();
    }
  }
}
