function log(s){
    console.log(s.toString())
}

function alert(s) {
    alert(s.toString())
}

var stdout = document.getElementById("code")

function println(s) {
    stdout.innerHTML += s.toString()+"<br>"
}

function print(s) {
    stdout.innerHTML += s
}



