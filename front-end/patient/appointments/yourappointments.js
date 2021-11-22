let myArray = [];
const { protocol, backend_ip, port, base_path } = API_CONFIG;

fetch(backend_url("/common/appointment"))
  .then((res) => res.text())
  .then((data) => {
    let json = JSON.parse(data);
    console.log(json["appointments"]);
    let details = json["appointments"];
    // // myarray = res.data
    // console.log(myArray)
    buildTable(details);
  });
let details = {
  appointments: [
    {
      location: "Himanshu ke ghar pr",
      name: "S4DGE",
      phone_number: "9874563211",
      time: "2021-11-03T11:30:00+00:00",
    },
    {
      location: "Rampur bushahar",
      name: "Windy",
      phone_number: "1236547891",
      time: "2021-11-01T10:00:00+00:00",
    },
  ],
};
function buildTable(details) {
  console.log(details);
  var table = document.getElementById("table1");

  for (var i = 0; i < details.length; i++) {
    var row = `<tr>
							<td>${details[i].name}</td>
							<td>${details[i].location}</td>
							<td>${details[i]["phone_number"]}</td>
							<td>${new Date(details[i].time).toLocaleString()}</td>
					  </tr>`;
    table.innerHTML += row;
  }
}

builtable(localStorage.getItem("name"));
function builtable(_data) {
  var table = document.getElementById("lol");
  table.innerHTML += "Hello ";
  table.innerHTML += _data;
}
