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

fetch(backend_url("/patients/order_medicine"), {
  method: "POST",
  body: toUrlEncoded(json),
  headers: {
    "Content-Type": "application/x-www-form-urlencoded",
  },
});
// below function prints the users name

buildTable(localStorage.getItem("name"));
function buildTable(data) {
  var table = document.getElementById("lol");
  table.innerHTML += "Hello ";
  table.innerHTML += data;
}
