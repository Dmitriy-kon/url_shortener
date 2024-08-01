export async function deleteUrl(urlId) {
  const response = await fetch(`/url/delete/?url_id=${urlId}`, {
    method: "DELETE",
  });

  if (response.ok) {
    const urlElement = document.getElementById(`url-${urlId}`);
    if (urlElement) {
      urlElement.remove();
    }
  } else {
    console.error("Ошибка при удалении URL:", response.statusText);
  }
}
