const { protocol, backend_ip, port, base_path } = API_CONFIG;

fetch(backend_url("/common/view_order_detail/"))
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
							<td>${details[i].patient_name}</td>
							<td>${details[i].location}</td>
							<td>${details[i].phone_number}</td>
							<td>${details[i].prescription["dose"]}</td>
							<td>${details[i].prescription["days"]}</td>
              <td>${details[i].prescription["medicine_name"]}</td>

					  </tr>`;
    table.innerHTML += row;
  }
}
