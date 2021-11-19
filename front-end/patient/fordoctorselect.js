[].forEach.call(document.querySelectorAll("lol"), function (input) {
  input.addEventListener("click", function (elm) {
    console.log(input.value);
    // Send this value to the server with ajax or something
  });
});

let form1 = document.getElementById("forall");
let form2 = document.getElementById("signup-form2");
let json = {};
form1.addEventListener("submit", (event) => {
  event.preventDefault();
  console.log(event);
  let form1_data = event;
  for (form_data_arr of new FormData(document.getElementById("forall"))) {
    json[form_data_arr[0]] = form_data_arr[1];
    console.log(form_data_arr);
  }
  console.log(json);
  console.log(JSON.stringify(json) + JSON.stringify(lol));
});

const toUrlEncoded = (obj) =>
  Object.keys(obj)
    .map((k) => encodeURIComponent(k) + "=" + encodeURIComponent(obj[k]))
    .join("&");
fetch("https://rica-remastered.herokuapp.com/api/v1/common/login", {
  method: "POST",
  body: toUrlEncoded(json),
  headers: {
    "Content-Type": "application/x-www-form-urlencoded",
  },
});

const myarray = [];
$.ajax({
  method: "GET",
  url: "https://reqres.in/api/users",
  success: function (response) {
    myArray = response.data;
    buildTable(myArray);
    console.log(myArray);
  },
});

$("#search-input").on("keyup", function () {
  var value = $(this).val();
  console.log("Value:", value);
  var data = searchTable(value, myArray);
  buildTable(data);
});

buildTable(myArray);

function searchTable(value, data) {
  var filteredData = [];
  for (var i = 0; i < data.length; i++) {
    value = value.toLowerCase();
    var name = data[i].last_name.toLowerCase();
    if (name.includes(value)) {
      filteredData.push(data[i]);
    }
  }
  return filteredData;
}

function buildTable(data) {
  var table = document.getElementById("myTable");
  table.innerHTML = "";
  for (var i = 0; i < data.length; i++) {
    var row = `<tr>
                        <td>${data[i].id}</td>

                        <td>${data[i].email}</td>

                        <td>${data[i].last_name}</td>


                   </tr>`;
    table.innerHTML += row;
  }
}
