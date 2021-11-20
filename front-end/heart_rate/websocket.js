Plotly.plot("chart", [
  {
    y: [],
    type: "line",
  },
]);

let gateway = "ws:/7fa4-112-196-163-170.ngrok.io/ws";

let websocket;
var cnt = 0;
// setInterval();
async function shift_plot_view() {
  // Plotly.extendTraces('chart',{ y:[[]]}, [0]);
  cnt++;
  if (cnt > 100) {
    Plotly.relayout("chart", {
      xaxis: {
        range: [cnt - 100, cnt],
      },
    });
  }
}

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

async function onMessage(event) {
  console.log(event.data);
  data = JSON.parse(event.data);
  if ("ir_val" in data) {
    Plotly.extendTraces("chart", { y: [[data["ir_val"]]] }, [0]);

    await shift_plot_view();
  }
}
