var myArray = [];

const { protocol, backend_ip, port, base_path } = API_CONFIG;
fetch(backend_url("/common/view_order_detail/")).then((response) => {
  console.log(response);
  buildTable(myArray);
  console.log(myArray);
});

function buildTable(data) {
  var table = document.getElementById("tbl-header");

  for (var i = 0; i < data.length; i++) {
    var row = `<tr>
							<td>${data[i].id}</td>
							<td>${data[i].last_name}</td>
							<td>${data[i].email}</td>
					  </tr>`;
    table.innerHTML += row;
  }
}
