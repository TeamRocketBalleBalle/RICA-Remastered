let form = document.getElementById("f1");
let json = {};
form.addEventListener("submit", (event) => {
  event.preventDefault();
  console.log(event);
  form1_data = event;
  for (form_data_arr of new FormData(document.getElementById("f1"))) {
    json[form_data_arr[0]] = form_data_arr[1];
  }

  // below line stores the username to the local storage
  setName_localSt(form_data_arr[1]);
  // console.log(getName_localSt());

  // TODO: debug print statement
  console.log(json);
  console.log(JSON.stringify(json));

  // source of wizardary: https://gist.github.com/lastguest/1fd181a9c9db0550a847
  const toUrlEncoded = (obj) =>
    Object.keys(obj)
      .map((k) => encodeURIComponent(k) + "=" + encodeURIComponent(obj[k]))
      .join("&");

  login_button = document.getElementsByClassName("login")[0];
  login_button.disabled = true;
  setTimeout(function () {
    login_button.disabled = false;
  }, 1500);

  fetch(backend_url("/common/login"), {
    method: "POST",
    body: toUrlEncoded(json),
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    credentials: "include",
  })
    .then((res) => res.text())
    .then((data) => {
      let json = JSON.parse(data);
      let success = false;
      if (json["status"] == "OK") {
        success = true;
      }
      if (json["usertype"] == "patient") {
        window.location.href = window.location.origin + "/patient/";
      }
      if (json["usertype"] == "doctor") {
        window.location.href = window.location.origin + "/doctor-select/";
        // window.location.href = "";
      }
      if (json["usertype"] == "chemist") {
        window.location.href = window.location.origin + "/chemist/";
      }

      display_error(json["reason"], success);
      login_button.disabled = false;
    })
    .catch((err) => {
      console.error(err);
      login_button.disabled = false;
    });
});

/* TODO: ideal function needed
      backend_url("/path") ==> heroku/path; ngrok.io/path */

let apiFormID = "API-input";
let apiForm = document.getElementById(apiFormID);

apiForm.addEventListener("submit", (event) => {
  event.preventDefault(); // prevent any default action
  let link = new FormData(document.getElementById(apiFormID)).get("API_URL");

  if (link == "") {
    console.error("link textbox is empty");
    display_error("link box is empty");
    return;
  }
  if (!validURL(link)) {
    console.error("link is not valud");
    display_error("link is not in right format");
    return;
  }

  // check if we get response from the url
  fetch(link + "/api/v1/ping")
    .then((res) => res.text())
    .then((data) => {
      if (data == "pong") {
        display_error("using <code>" + link + "</code> as backend URL", true);
        localStorage.setItem(API_CONFIG.KEY_NAME, link);
      }
    })
    .catch((err) => {
      console.error(err);
      display_error("not valid API url");
      document.getElementById("API_URL").textContent = "";
    });
});

function display_error(msg, success = false) {
  body = document.getElementsByTagName("body")[0];
  let error_div = document.getElementsByClassName("alert")[0];
  if (error_div == null) {
    error_div = document.createElement("div");
    error_div.classList.add("alert");
    if (success) {
      error_div.classList.add("alert-success");
    } else {
      error_div.classList.add("alert-danger");
    }
  }

  error_div.innerHTML = msg;
  // error_html = `<div class="alert alert-danger" role="alert">${msg}</div>`;
  setTimeout(function () {
    error_div.parentNode.removeChild(error_div);
  }, 5000);
  body.prepend(error_div);
}

// source: https://stackoverflow.com/a/5717133
function validURL(str) {
  var pattern = new RegExp(
    "^(https?:\\/\\/)" + // protocol
      "((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|" + // domain name
      "((\\d{1,3}\\.){3}\\d{1,3}))" + // OR ip (v4) address
      "(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*" + // port and path
      "(\\?[;&a-z\\d%_.~+=-]*)?" + // query string
      "(\\#[-a-z\\d_]*)?$",
    "i"
  ); // fragment locator
  return !!pattern.test(str);
}

// below code stores usernames to the local storage
function setName_localSt(_name) {
  localStorage.setItem("name", _name);
}
function getName_localSt() {
  return localStorage.getItem("name");
}
