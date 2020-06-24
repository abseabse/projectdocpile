// CONTROLLER MODULE

// PRESENTER MODULE

// HTML modifyer block
async function addEventsToDocs() {
  // adds events to docs
  let docList = document.getElementsByClassName('doc');
  for (let doc of docList) {
    // adds links to docs
    getDoc(doc.id).then(function(value) {
      doc.setAttribute('href', value);
    });
    // Here goed strings of code that makes the same, but sequentedly:
    // let docFromBase = await getDoc(doc.id);
    // doc.setAttribute('href', docFromBase);
    // adds selection to docs
    doc.onclick = function() {
      doc.classList.toggle('selected');
      let newDocList = document.getElementsByClassName('doc');
      for (let newDoc of newDocList) {
        if (newDoc != doc) {
          newDoc.classList.remove('selected');
        }
      }
    };
    // opens doc properties in a modal window
    doc.ondblclick = function(event) {
      document.getElementById('modal_doc_name').value = event.target.innerHTML;
      document.getElementById('modal_doc_id').value = event.target.id;
      document.getElementById('modal_doc_link').value = event.target.getAttribute('href');
      let modal = document.getElementById('doc_window');
      modal.style.display = "block";
    };
  }
}

// CONTROLLER FUNCTIONS
async function getDoc(doc_id) {
  let response = await fetch('http://localhost/projectdocpile/cgi-bin/update_task.py', {
                                method: 'POST',
                                body: JSON.stringify({userAction: 'get doc', docId: doc_id})
                                });
  if (response.ok) {
    let doc = await response.json();
    return doc.doc_link;
  } else {
      alert("Ошибка HTTP: " + response.status);
  }
}

async function addDoc() {
  let taskId = document.getElementsByClassName('selected')[0].id;
  let response = await fetch('http://localhost/projectdocpile/cgi-bin/update_task.py', {
                                method: 'POST',
                                body: JSON.stringify({userAction: 'add doc', docName: 'new doc', taskId:taskId})
                                });
  if (response.ok) {
    response.text().then(function(json) {
      // FIXME debugging
      let docList = document.getElementById('docs_list');
      let node = document.createElement('li');
      node.id = json.doc_id;
      node.classList.add("doc");
      let text = document.createTextNode("new doc");
      node.appendChild(text);
      docList.appendChild(node);
      // addEventsToDocs();
    });
  } else {
    alert("Ошибка HTTP: " + response.status);
  }
}

async function updateDoc(doc) {
  let docName = doc.doc_name.value;
  let docId = doc.doc_id.value;
  let docLink = doc.doc_link.value;
  let response = await fetch('http://localhost/projectdocpile/cgi-bin/update_task.py', {
                                method: 'POST',
                                body: JSON.stringify({userAction: 'update doc', docName: docName, docId: docId, docLink: docLink})
                                });
  if (response.ok) {
    response.text().then(function(json) {
      // TODO insert some code here in the future
    });
  } else {
    alert("Ошибка HTTP: " + response.status);
  }
}

async function updateTask(task) {
  let taskName = task.task_name.value;
  let taskId = task.task_id.value;
  let response = await fetch('http://localhost/projectdocpile/cgi-bin/update_task.py', {
                                method: 'POST',
                                body: JSON.stringify({userAction: 'update task', taskName: taskName, taskId: taskId})
                                });
  if (response.ok) {
    response.text().then(function(json) {
      // TODO place some code here
    });
  } else {
      alert("Ошибка HTTP: " + response.status);
  }
}
