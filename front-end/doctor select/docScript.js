var upButton = document.getElementById("upButton");
var downButton = document.getElementById("downButton");
var circle = document.getElementById("circle");

var rotate = circle.style.transform;
var sum;

upButton.onclick = function () {
  sum = rotate + "rotate(-180deg)";
  circle.style.transform = sum;
  rotate = sum;
};

downButton.onclick = function () {
  sum = rotate + "rotate(180deg)";
  circle.style.transform = sum;
  rotate = sum;
};
// below function prints the users name

buildTable(localStorage.getItem("name"));
function buildTable(data) {
  var table = document.getElementById("lol");
  table.innerHTML += "Hello ";
  table.innerHTML += data;
}
