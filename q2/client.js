function replace_user_list (users) {
  select = document.getElementById('user-list')
  select.innerHTML = ""
  for (var i = users.length - 1; i >= 0; i--) {
    user = users[i]
    select.innerHTML += "<option" + (user.selected ? " selected=true": "") +
     ">" + user.username + "</option>"
  }
}

function handle_user_response(){
  users = JSON.parse(this.responseText)
  replace_user_list(users)
}

function get_users(users) {
  user_request = new XMLHttpRequest()
  user_request.onload = handle_user_response 
  user_request.open('GET', 'users.cgi')
  user_request.send()
}

window.onload = function(){
  console.log("loaded!")
  get_users()
}
