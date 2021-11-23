const API_CONFIG = {
  protocol: "http",
  backend_ip: "rica.trballeballe.ml",
  base_path: "/api/v1",
  KEY_NAME: "API_URL",
};

function backend_url(path) {
  if (localStorage.getItem(API_CONFIG.KEY_NAME) == null) {
    return (
      API_CONFIG.protocol +
      "://" +
      API_CONFIG.backend_ip +
      API_CONFIG.base_path +
      path
    );
  } else {
    return (
      localStorage.getItem(API_CONFIG.KEY_NAME) + API_CONFIG.base_path + path
    );
  }
}
