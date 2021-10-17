var upButton = document.getElementById("upButton")
var downButton = document.getElementById("downButton")
var circle = document.getElementById("circle")

var rotate = circle.style.transform;
var sum;


upButton.onclick = function()
{
    sum = rotate + "rotate(-90deg)"
    circle.style.transform = sum;
    rotate = sum;
}

downButton.onclick = function()
{
    sum = rotate + "rotate(90deg)"
    circle.style.transform = sum;
    rotate = sum;
}

