Plotly.plot("chart", [
  {
    y: [],
    type: "line",
  },
]);

let gateway = "ws://192.168.1.38/ws";
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
    Plotly.extendTraces("chart", { y: [[data["ir_val"]]] }, [0]);
  }
}
