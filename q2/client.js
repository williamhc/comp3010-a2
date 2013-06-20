function replace_user_list (users) {
  select = document.getElementById('user-list')
  select.innerHTML = ""
  selected = users[0]
  for (var i = 0; i < users.length; i++) {
    user = users[i]
    select.innerHTML += "<option" + (user.selected ? " selected=true": "") +
     ">" + user.username + "</option>"
    if (user.selected) {
      selected = user
    }
  }
  //return the selected user
  return selected
}

function handle_user_response(){
  users = JSON.parse(this.responseText)
  selected = replace_user_list(users)
  // now we know which one is selected and which tasks to show
  get_tasks(selected)
}

function get_users() {
  user_request = new XMLHttpRequest()
  user_request.onload = handle_user_response
  user_request.open('GET', 'users.cgi')
  user_request.send()
}

function replace_task_list (tasks) {
  tbody = document.getElementById('task-list')
  tbody.innerHTML = ""
  for (var i = tasks.length - 1; i >= 0; i--) {
    task = tasks[i]
    tbody.innerHTML += "<tr><td>" + task.user + "</td><td>" + task.priority +
      "</td><td>" + task.title + "</td><td>" + task.description + 
      "</td><td>" + make_delete_button(task) + "<td></tr>"
  }
  delete_btns = document.getElementsByClassName('delete-task-btn')
  for (var i = 0; i < delete_btns.length; i++) {
    btn = delete_btns[i]
    btn.onclick = delete_task
  }
}

function make_delete_button(task){
  return "<button class='btn delete-task-btn'" +
    "data-task-id='" + task.id + "'><i class='icon-trash'></i></button>"
}

function delete_task(e){
  id = e.currentTarget.getAttribute('data-task-id')
  delete_request = new XMLHttpRequest()
  delete_request.onload = get_users
  delete_request.open('DELETE', 'tasks.cgi?id=' + id)
  delete_request.send()
}

function on_user_changed(e){
  get_tasks({'username': e.target.selectedOptions[0].value})
}

function handle_task_response(){
  tasks = JSON.parse(this.responseText)
  replace_task_list(tasks)
}

function get_tasks(user) {
  task_request = new XMLHttpRequest()
  task_request.onload = handle_task_response
  task_request.open('GET', 'tasks.cgi' + (user ? '?user=' + user.username : ''))
  task_request.send()
}

function toggle_form(){
  form_area = document.getElementById('new-task-form')
  if(form_area.childElementCount == 0){
    contents = document.getElementById('form-template').innerHTML
  }else{
    contents = ""
  }
  form_area.innerHTML = contents
}

window.onload = function(){
  get_users()
  new_but = document.getElementById('new-task-button')
  new_but.onclick = toggle_form
  select = document.getElementById('user-list')
  select.onchange = on_user_changed
  
}

