import { postAddLink } from "./postAddLink.js";
import { deleteUrl } from "./deletelink.js";
import { generateShortUrl } from "./generate.js";
import { copyToClipboard } from "./copy_to_clipboard.js";

export async function login(username, password) {
  const params = new URLSearchParams();
  params.append("username", username);
  params.append("password", password);

  const response = await fetch("/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: params.toString(),
  });

  if (response.ok) {
    const data = await response.json();
    document.cookie = `Bearer=${data.token}; path=/`;
    return true;
  } else if (response.status === 422) {
    const errorData = await response.json();
    alert(`${errorData.detail[0].msg} in ${errorData.detail[0].loc[1]}`);
  } else {
    const errorData = await response.json();
    alert(errorData.message);
    return false;
  }
}

export async function signup(username, password) {
  const params = new URLSearchParams();
  params.append("username", username);
  params.append("password", password);

  const response = await fetch("/auth/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: params.toString(),
  });

  if (response.ok) {
    return await login(username, password);
  } else if (response.status === 422) {
    const errorData = await response.json();
    alert(`${errorData.detail[0].msg} in ${errorData.detail[0].loc[1]}`);
  } else {
    const errorData = await response.json();
    console.log(errorData);
    alert(errorData.message);
    return false;
  }
}

export async function fetchUrls() {
  const response = await fetch("/url/all", {
    method: "GET",
  });

  if (response.ok) {
    const html = await response.text();
    document.getElementById("response-div").innerHTML = html;
    addDeleteEventListeners(); // Добавляем обработчики событий для кнопок удаления
    addPostEventListeners();
    addGenerateEventListeners();
    addCopyEventListeners();
  } else {
    console.error("Ошибка при загрузке URL:", response.statusText);
  }
}

function addDeleteEventListeners() {
  document.querySelectorAll(".delete-button").forEach((button) => {
    button.addEventListener("click", async (event) => {
      const urlId = event.target.getAttribute("data-url-id");
      if (urlId) {
        await deleteUrl(urlId);
        await fetchUrls();
      }
    });
  });
}

function addPostEventListeners() {
  document
    .getElementById("add-url-button")
    .addEventListener("click", async () => {
      await postAddLink();
      await fetchUrls();
    });
}
// function addGenerateEventListeners() {
//   document.querySelectorAll(".generate-button").forEach((button) => {
//     button.addEventListener("click", async (event) => {
//       const urlId = event.target.getAttribute("data-url-id");
//       if (urlId) {
//         await generateShortUrl(urlId);
//         // await fetchUrls();
//       }
//     });
//   });
// }


function addGenerateEventListeners() {
  document.querySelectorAll(".generate-button").forEach((button) => {
      button.addEventListener("click", async (event) => {
          const urlId = event.target.getAttribute("data-url-id");
          if (urlId) {
              await generateShortUrl(urlId);
          }
      });
  });
}
function addCopyEventListeners() {
  document.querySelectorAll(".copy-button").forEach((button) => {
    button.addEventListener("click", async (event) => {
      const url = event.target.getAttribute("data-url");
      if (url) {
        await copyToClipboard(url);
        alert("Ссылка скопирована в буфер обмена!");
      }
    });
  });
}
