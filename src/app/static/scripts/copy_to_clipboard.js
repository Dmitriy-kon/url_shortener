export async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        console.log('Ссылка скопирована в буфер обмена');
    } catch (err) {
        console.error('Не удалось скопировать текст: ', err);
    }
}
