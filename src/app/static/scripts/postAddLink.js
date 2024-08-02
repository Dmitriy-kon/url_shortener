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
  } else if (response.status === 422) {
    const errorData = await response.json();
    alert(`${errorData.detail[0].msg} in ${errorData.detail[0].loc[1]}`);
  } else {
    alert(await response.json().then((data) => data.message));
    console.log("Error");
  }
}
