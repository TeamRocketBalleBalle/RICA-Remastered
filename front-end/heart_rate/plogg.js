console.log("jhi");
let gateway = "ws://8e39-112-196-163-170.ngrok.io/ws";
let websocket;

// ----------------------------------------------------------------------------
// Initialization
// ----------------------------------------------------------------------------

// window.addEventListener("load", onLoad);

function onLoad(event) {
  initWebSocket();
}

// ----------------------------------------------------------------------------
// WebSocket handling
// ----------------------------------------------------------------------------

function initWebSocket() {
  console.log("Trying to open a WebSocket connection...");
  websocket = new WebSocket(gateway);
  websocket.onopen = onOpen;
  websocket.onmessage = onMessage;
  // websocket.onclose = onClose;
}

function onOpen(event) {
  console.log("Connection opened");
}

function onClose(event) {
  console.log("Connection closed");
  setTimeout(initWebSocket, 2000);
}

function onMessage(event) {
  console.log(event.data);
  data = JSON.parse(event.data);
  if ("ir_val" in data) {
    div = document.getElementById("log");
    // div.textContent += "\n" + event.data;
    ydata = JSON.parse(event.data);
    // return ydata;
    // div.scrollIntoView(false);
  }
  // if ("bpm" in data) {
  //   bpm = document.getElementById("bpm");
  //   bpm.textContent = "BPM: " + JSON.stringify(data);
  // }
}
let ydata = [];
var is_fetched = false;
initWebSocket();
// $.ajax({
//   method: "GET",
//   url: "https://reqres.in/api/users",
//   success: function (response) {
ydata = response.data.map((data) => onMessage());
is_fetched = true;
//   },
// });
// function buildTable() {
//     return Math.random();
// }

Plotly.plot("chart", [
  {
    y: [],
    type: "line",
  },
]);

var cnt = 0;

setInterval(function () {
  if (is_fetched) {
    Plotly.extendTraces(
      "chart",
      {
        y: [ydata],
      },
      [0]
    );
    cnt++;
    if (cnt > 500) {
      Plotly.relayout("chart", {
        xaxis: {
          range: [cnt - 500, cnt],
        },
      });
    }
  }
}, 200);
