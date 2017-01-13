function log(s){
    console.log(s.toString())
}

var stdout = document.getElementById("code")

function println(s) {
    stdout.innerHTML += s.toString()+"<br>"
}

function print(s) {
    stdout.innerHTML += s
}

function println_unop(s, next) {
    stdout.innerHTML += s.toString()+"<br>"
    next();
}

function print_unop(s, next) {
    stdout.innerHTML += s
    next();
}




