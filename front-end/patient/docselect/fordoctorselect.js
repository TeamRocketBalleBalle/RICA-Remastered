// $.ajax({
//   method: "GET",
//   url: backend_url("common/patients"),
//   success: function (response) {
//     myArray = response.data;
//     buildtable(myArray);
//     console.log(myArray);
//   },
// });
//
builtable(localStorage.getItem("name"));
function builtable(_data) {
  var table = document.getElementById("lol");
  table.innerHTML += "Hello ";
  table.innerHTML += _data;
}

let myArray = [];
const { protocol, backend_ip, port, base_path } = API_CONFIG;

fetch(backend_url("/patients/get_doctors/"))
  .then((res) => res.text())
  .then((data) => {
    let json = JSON.parse(data);
    console.log(json["doctor_details"]);
    let details = json["doctor_details"];
    // // myarray = res.data
    // console.log(myArray)
    buildTable(details);
  });

function buildTable(details) {
  var table = document.getElementById("myTable");

  for (var i = 0; i < details.length; i++) {
    var row = `<tr>
							<td>${details[i].doctor_id}</td>
							<td>${details[i].doctor_name}</td>
							<td>${details[i].location}</td>
							<td>${details[i].phone}</td>
							<td>${details[i].email}</td>
					  </tr>`;
    table.innerHTML += row;
  }
}
let id = [];
document.querySelectorAll(".radio-buttons").forEach((radio) => {
  radio.addEventListener("click", () => {
    id = radio.parentElement.getAttribute(data - id);
    id.innerHTML = data - id;
  });
});
//above code for radio button

let form1 = document.getElementById("forall");
let json = {};
form1.addEventListener("submit", (event) => {
  event.preventDefault();
  // console.log(event);
  let form1_data = event;
  for (form_data_arr of new FormData(document.getElementById("forall"))) {
    json[form_data_arr[0]] = form_data_arr[1];
    console.log(form_data_arr);
  }
  console.log(json);
  console.log(JSON.stringify(json));
});

const toUrlEncoded = (obj) =>
  Object.keys(obj)
    .map((k) => encodeURIComponent(k) + "=" + encodeURIComponent(obj[k]))
    .join("&");
fetch(backend_url("/patients/new_appointment/"), {
  method: "POST",
  body: toUrlEncoded(json),
  headers: {
    "Content-Type": "application/x-www-form-urlencoded",
  },
});
//post data

//above where we get data

$("#search-input").on("keyup", function () {
  var value = $(this).val();
  console.log("Value:", value);
  var data = searchTable(value, json);
  buildTable(data);
});

buildTable(details);
//search attribute
function searchTable(value, data) {
  var filteredData = [];
  for (var i = 0; i < details.length; i++) {
    value = value.toLowerCase();
    var name = details[i].doctor_name.toLowerCase();
    if (name.includes(value)) {
      filteredData.push(data[i]);
    }
  }
  return filteredData;
} //still control

function buildTable(details) {
  var table = document.getElementById("myTable");

  for (var i = 0; i < details.length; i++) {
    var row = `<tr>
							<td>${details[i].name}</td>
							<td>${details[i].location}</td>
							<td>${details[i].phone}</td>
							<td>${details[i].time}</td>
					  </tr>`;
    table.innerHTML += row;
  }
}

// function click(){
//   alert("APPOINTMENT BOOKED")
// }
