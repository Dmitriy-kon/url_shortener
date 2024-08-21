// export async function generateShortUrl(urlId) {
//     const response = await fetch(`/url/change/?url_id=${urlId}`, {
//       method: "PATCH",
//     });

//     if (response.ok) {
//       const urlElement = document.getElementById(`short-url${urlId}`);
//       if (urlElement) {
//         urlElement.innerHTML.replace = await response.text();
//       }
//     } else {
//       console.error("Ошибка при удалении URL:", response.statusText);
//     }
//   }
export async function generateShortUrl(urlId) {
  const response = await fetch(`/url/change/?url_id=${urlId}`, {
    method: "PATCH",
  });

  if (response.ok) {
    // let newShortUrl = await response.text();
    // newShortUrl = newShortUrl.replace(/"/g, '');
    let newShortUrl = await response.json().then((data) => data.short_url);

    // Обновляем ссылку
    const urlElement = document.getElementById(`short-url${urlId}`);
    if (urlElement) {
      urlElement.href = newShortUrl;
    }

    // Обновляем кнопку копирования
    const copyButton = document.getElementById(`copy-url${urlId}`);

    // const copyButton = document.querySelector(
    //   `.copy-button[data-url-id="${urlId}"]`
    // );
    if (copyButton) {
      copyButton.setAttribute("data-url", newShortUrl);
    }
  } else {
    console.error("Ошибка при изменении URL:", response.statusText);
  }
}
