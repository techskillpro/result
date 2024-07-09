const getResult = () => {
    let math = document.getElementById('math').value;
    let physics = document.getElementById('physics').value;
    let chemistry = document.getElementById('chemistry').value;
    let c = document.getElementById('cprogramming').value;
    let python = document.getElementById('python').value;

    if(document.getElementsByTagName('input').value==""){
        alert("Please Enter Some Value");
    }
    let total = parseFloat(math) + parseFloat(physics) + parseFloat(chemistry) + parseFloat(c) + parseFloat(python);
    let percentage = (total * 100) / 500;

    if (percentage >= 90) {
        document.getElementById("grade").innerHTML = "A+";
    }
    else if (percentage >= 80) {
        document.getElementById("grade").innerHTML = "A";

    }
    else if (percentage >= 70) {
        document.getElementById("grade").innerHTML = "B";

    }
    else if (percentage >= 60) {
        document.getElementById("grade").innerHTML = "C";

    }
    else if (percentage >= 50) {
        document.getElementById("grade").innerHTML = "D";

    }
    else if (percentage >= 35) {
        document.getElementById("grade").innerHTML = "E";

    }
    else {
        document.getElementById("grade").innerHTML = "You Are Failed";

    }
    document.getElementById('percentage').innerHTML = percentage;
    document.getElementById('total').innerHTML = total;
}