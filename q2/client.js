function replace_user_list (users) {
  select = document.getElementById('user-list')
  select.innerHTML = ""
  for (var i = users.length - 1; i >= 0; i--) {
    user = users[i]
    select.innerHTML += "<option" + user.selected ? " selected=true": "" +
     ">" + user.name + "</option>"
  }
}

function get_users(users) {
  user_request = new XMLHttpRequest({
    onload: function(){
      users = JSON.parse(this.responseText)
      replace_user_list(users)
    }
  })
  user_request.open('GET', 'users.cgi')
  user_request.send()
}

window.onload = function(){
  console.log("loaded!")
  get_users()
}
