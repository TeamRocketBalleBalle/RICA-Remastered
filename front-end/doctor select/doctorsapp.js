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

builtable(localStorage.getItem("name"));
function builtable(_data) {
  var table = document.getElementById("lol");
  table.innerHTML += "Hello ";
  table.innerHTML += _data;
}

function buildTable(details) {
  var table = document.getElementById("myTable");

  for (var i = 0; i < details.length; i++) {
    var row = `<tr>
							<td>${details[i].patient_name}</td>
							<td>${details[i].location}</td>
							<td>${details[i].phone_number}</td>
							<td>${new Date(details[i].time).toLocaleString()}</td>
					  </tr>`;
    table.innerHTML += row;
  }
}
