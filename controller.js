// Controller module
import * as model from './model.js';
import * as presenter from './presenter.js';


export async function updateTasks() { 
  let taskList = await model.getTaskList();
  let docList = model.getDocList;
  let taskInfo = model.getTaskInfo;
  await presenter.updateTasks(taskList, docList, taskInfo);
}

export async function updateDocs(taskId) {
  let docList = await model.getDocList(taskId=taskId);
  presenter.updateDocs(docList);
}

export async function addTask() {
  let taskAdded = await model.addTask();
  let getDocList = model.getDocList;
  presenter.addTask(taskAdded, getDocList);
}

export async function modifyTask(task) {
  let taskId = task.modal_task_id.value;
  let taskProperties = new Object;
  taskProperties.task_name = await task.modal_task_name.value;
  await model.modifyTask(taskId, taskProperties);
  presenter.modifyTask(taskId, taskProperties);
}

export function deleteTask(taskId) {
  let getDocList = model.getDocList;
  model.deleteTask(taskId);
  presenter.deleteTask(taskId, getDocList);
  // prevents main window from reloading after user presses the delete button 
  return false;
}

export async function addDoc(docProperties) {
  let selectedTask = await presenter.getSelectedTask();
  let selectedTaskId = undefined;
  if (selectedTask) {
    selectedTaskId = selectedTask.id;
  }
  let docAdded = await model.addDoc(selectedTaskId);
  await console.log(docAdded);
  presenter.addDoc(docAdded);
}

export async function modifyDoc(docId, docProperties) {
  let docModified = await model.modifyDoc(docId, docProperties);
  console.log(docModified);
  presenter.modifyDoc(docId, docProperties);
}

export async function deleteDoc() {
  let SelectedDocId = await presenter.getDocSelected();
  if (SelectedDocId) {
    model.deleteDoc(SelectedDocId);
    presenter.deleteDoc(SelectedDocId);  
  }
}

export function mainLoad() {
  updateTasks();
  presenter.mainLoad();
}

