$.ajax({
  method: "GET",
  url: "https://reqres.in/api/users",
  success: function (response) {
    myArray = response.data;
    buildTable(myArray);
    console.log(myArray);
  },
});
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

function buildTable(data) {
  var table = document.getElementById("lol");

  for (var i = 0; i < data.length; i++) {
    var name = `${data[i].id}`;
    table.innerHTML += name;
  }
}
