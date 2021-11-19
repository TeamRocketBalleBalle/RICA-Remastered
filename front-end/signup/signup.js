let form1 = document.getElementById("gg");
let form2 = document.getElementById("signup-form2");
let json = {};
form1.addEventListener("submit", (event) => {
  event.preventDefault();
  console.log(event);
  form1_data = event;
  for (form_data_arr of new FormData(document.getElementById("signup-form"))) {
    json[form_data_arr[0]] = form_data_arr[1];
  }
  console.log(json);
  console.log(JSON.stringify(json));
});
const toUrlEncoded = (obj) =>
  Object.keys(obj)
    .map((k) => encodeURIComponent(k) + "=" + encodeURIComponent(obj[k]))
    .join("&");
fetch("https://rica-remastered.herokuapp.com/api/v1/common/login", {
  method: "POST",
  body: toUrlEncoded(json),
  headers: {
    "Content-Type": "application/x-www-form-urlencoded",
  },
})
  .then((res) => res.text())
  .then((html) => console.log(html))
  .catch((err) => console.error(err));

// var ViewModel = function() {
//   var self = this;
//
//   self.showGrid = ko.observable(true);
//   self.toggleView = function() {
//     self.showGrid(!self.showGrid());
//   }
// }
//
// var vm = new ViewModel();
// ko.applyBindings(vm);
