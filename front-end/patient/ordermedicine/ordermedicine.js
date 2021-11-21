$.ajax({
  method: "GET",
  url: "https://reqres.in/api/users",
  success: function (response) {
    myArray = response.data;
    buildTable(myArray);
    console.log(myArray);
  },
});

let form1 = document.getElementById("formlol");
let json = {};
form1.addEventListener("submit", (event) => {
  event.preventDefault();
  console.log(event);
  let form1_data = event;
  for (form_data_arr of new FormData(document.getElementById("formlol"))) {
    json[form_data_arr[0]] = form_data_arr[1];
    console.log(form_data_arr);
  }
  console.log(json);
  console.log(JSON.stringify(json));
});
//code to convert data
const toUrlEncoded = (obj) =>
  Object.keys(obj)
    .map((k) => encodeURIComponent(k) + "=" + encodeURIComponent(obj[k]))
    .join("&");
fetch("link where we post data", {
  method: "POST",
  body: toUrlEncoded(json),
  headers: {
    "Content-Type": "application/x-www-form-urlencoded",
  },
});

function buildTable(data) {
  var table = document.getElementById("lol");

  for (var i = 0; i < data.length; i++) {
    var name = `${data[i].id}`;
    table.innerHTML += name;
  }
}
