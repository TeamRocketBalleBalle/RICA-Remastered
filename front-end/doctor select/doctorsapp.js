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
