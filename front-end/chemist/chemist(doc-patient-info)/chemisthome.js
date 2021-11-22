const { protocol, backend_ip, port, base_path } = API_CONFIG;

fetch(backend_url("/common/view_order_details/"))
  .then((res) => res.text())
  .then((data) => {
    let json = JSON.parse(data);
    console.log(json["order_details"]);
    let details = json["order_details"];

    buildTable(details);
  });

function buildTable(details) {
  var table = document.getElementById("tbl-header");

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
