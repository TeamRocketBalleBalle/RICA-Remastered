$.ajax({
  method: "GET",
  url: "https://reqres.in/api/users",
  success: function (response) {
    myArray = response.data;
    buildtable(myArray);
    console.log(myArray);
  },
});

var myArray = [];

$.ajax({
  method: "GET",
  url: "https://reqres.in/api/users",
  success: function (response) {
    myArray = response.data;
    buildTable(myArray);
    console.log(myArray);
  },
});

function buildTable(data) {
  var table = document.getElementById("myTable");

  for (var i = 0; i < data.length; i++) {
    var row = `<tr>
							<td>${data[i].id}</td>
							<td>${data[i].last_name}</td>
							<td>${data[i].email}</td>
					  </tr>`;
    table.innerHTML += row;
  }
}

function buildtable(data) {
  var table = document.getElementById("lol");

  for (var i = 0; i < data.length; i++) {
    var name = `${data[i].id}`;
    table.innerHTML += name;
  }
}
