const wifi = fetch("")
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
    wifi_table(data);
  });

function wifi_table(data) {
  const names = document.getElementById("wifi_name");

  for (var i = 0; i < data.length; i++) {
    const row = `<tr>
                 <td>${data[i].SSID}</td>
                 <td>${data[i].RSSI}</td>
                 <tr>`;
    names.innerHTML += row;
  }
}
let esp_ip = "http://bc2c-103-61-113-250.ngrok.io";
let ssid = document.getElementById("name").value;
let password = document.getElementById("password").value;
let encodedSSID = escape(unescape(encodeURIComponent(ssid)));
let encodedPASS = escape(unescape(encodeURIComponent(password)));
let url =
  esp_ip + "/accept_credentials?SSID=" + encodedSSID + "&PASS=" + encodedPASS;
console.log(url);

fetch(url),
  {
    method: "post",
    headers: {
      Accept: "application/json, text/plain, */*",
      "Content-Type": "application/json",
    },
  };

//status

let status1, codi;

fetch(url)
  .then((response) => response.json)
  .then((data) => {
    console.log(data);
    status0(data);
  });

function status0(data) {
  status1 = data.status;
  if (status1 === "1") alert("Invalid pass");
  if (status1 === "2") alert("NO SSID");
  if (status1 === "3") alert("Connecting");
  if (status1 === "4") alert("connected");
  else alert("no credentials");
}

//client code
let form = document.getElementById("bumton");

form.addEventListener("submit", (event) => {
  event.preventDefault();
  console.log(event);
  let fd = event;
  for (fda of new FormData(document.getElementById("bumton"))) {
    json[fda[0]] = fda[1];
  }
  console.log(json);
  console.log(JSON.stringify(json));
  fetch(url),
    {
      method: "post",
      headers: {
        Accept: "application/json, text/plain, */*",
        "Content-Type": "application/json",
      },
      body: json.stringify({ code: "200", sstr: "OK" }),
    };
});
