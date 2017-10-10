//ajax函数
var ajax = function (method, path, data, responseCallback) {
    var r = new XMLHttpRequest()
    //设置响应的方法和请求地址
    r.open(method, path, true)
    //设置请求希望得到的类型
    r.setRequestHeader('Content-Type', 'application/json')
    //注册响应函数
    r.onreadystatechange = function () {
        if (r.readyState === 4) {
            //r.response存的就是服务器发过来存在body中的数据
            responseCallback(r.response)
        }
    }
    data = JSON.stringify(data)
    r.send(data)
}

//模版函数
var template = function (data) {
    return '<span>' + data + '</span><button>删除</button>'
}

//插入一条数据
var insertIntoLast = function (data) {
    document.querySelector('.item').insertAdjacentHTML('beforeend', template(data))
}

var bindToAdd = function () {
    var btn = document.querySelector('#user-add')
    btn.addEventListener('click', function () {
        var username = document.querySelector('#username').value
        var password_hash = document.querySelector('#password_hash').value
        var data = {
            username: username,
            password_hash: password_hash
        }
        ajax('POST', '/api/add', data, function (user_str) {
            user = JSON.parse(user_str)
            insertIntoLast(user['username'] + user['password_hash'])
        })
    })
}

//加载所有用户信息
var loadUsers = function () {
    ajax('GET', '/api/all', '', function (response) {
        var users = JSON.parse(response)
        for (var i = 0; i < users.length; i++) {
            var user = users[i]
            console.log(user)
            insertIntoLast(user.username + user.password_hash)
        }
    })
}

bindToAdd()
loadUsers()