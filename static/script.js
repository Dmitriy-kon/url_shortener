// import htmx from "htmx.org";
import { postAddLink } from "./scripts/postAddLink.js";
import { deleteUrl } from "./scripts/deletelink.js";
import { login, signup, fetchUrls } from "./scripts/auth.js";
// function postAddLink() {
//   let headers = {
//     "Content-Type": "application/json",
//   };
//   let body = {
//     url: document.getElementById("new-url").value,
//   };
//   console.log(body);

//   // htmx.ajax("POST", "/url/insert", { headers: headers }, body);
//   fetch("/url/insert", {
//     method: "POST",
//     headers: headers,
//     body: JSON.stringify(body),
//   })
//     .then((response) => {
//       if (response.ok) {
//         window.location.href = "/url/all";
//       } else {
//         console.log("Error");
//       }
//     })
//     .catch((error) => {
//       console.log(error);
//     });
// }
document.addEventListener("DOMContentLoaded", async () => {
  if (getCookie("Bearer")) {
    await fetchUrls();
  }

  document
    .getElementById("login-button")
    .addEventListener("click", async () => {
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;
      const success = await login(username, password);
      if (success) {
        await fetchUrls();
      }
    });

  document
    .getElementById("signup-button")
    .addEventListener("click", async () => {
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;
      const success = await signup(username, password);
      if (success) {
        await fetchUrls();
      }
    });
});

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

// document
//   .getElementById("add-url-button")
//   .addEventListener("click", postAddLink);

// document.addEventListener("DOMContentLoaded", () => {
//   document.querySelectorAll(".delete-button").forEach((button) => {
//     button.addEventListener("click", (event) => {
//       const urlId = event.target.getAttribute("data-url-id");
//       if (urlId) {
//         deleteUrl(urlId);
//       }
//     });
//   });
// });
