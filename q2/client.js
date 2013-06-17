function replace_user_list (users) {
  select = document.getElementById('user-list')
  select.innerHTML = ""
  for (var i = users.length - 1; i >= 0; i--) {
    user = users[i]
    select.innerHTML += "<option" + (user.selected ? " selected=true": "") +
     ">" + user.username + "</option>"
    if (user.selected) {selected = user};
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
      "</td><td>" + task.title + "</td><td>" + task.description + "</td></tr>"
  }
}

function handle_task_response(){
  tasks = JSON.parse(this.responseText)
  replace_task_list(tasks)
}

function get_tasks(user) {
  task_request = new XMLHttpRequest()
  task_request.onload = handle_task_response
  task_request.open('GET', 'tasks.cgi' + (user ? '?user=' + user.name : ''))
  task_request.send()
}

window.onload = function(){
  console.log("loaded!")
  get_users()
  get_tasks()
}
