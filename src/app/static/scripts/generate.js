export async function generateShortUrl(urlId) {
    const response = await fetch(`/url/change/?url_id=${urlId}`, {
      method: "PATCH",
    });

    if (response.ok) {
      const urlElement = document.getElementById(`short-url${urlId}`);
      if (urlElement) {
        urlElement.innerHTML = await response.text();
      }
    } else {
      console.error("Ошибка при удалении URL:", response.statusText);
    }
  }
