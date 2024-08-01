// import { postAddLink } from "./postAddLink.js";
// import { deleteUrl } from "./deletelink.js";
export async function postAddLink() {
  let headers = {
    "Content-Type": "application/json",
  };
  let body = {
    url: document.getElementById("new-url").value,
  };

  const response = await fetch("/url/insert", {
    method: "POST",
    headers: headers,
    body: JSON.stringify(body),
  });

  if (response.ok) {
    const html = await response.text();
  } else {
    console.log("Error");
  }
}
