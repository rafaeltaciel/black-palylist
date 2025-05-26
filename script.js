const downloadButton = document.querySelector('button');
const input = document.querySelector('input');

downloadButton.addEventListener('click', async () => {
    const url = input.value.trim();

    if (!url) {
        alert('Por favor, cole o link da playlist.');
        return;
    }

    try {
        const response = await fetch('/download_playlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message);
        } else {
            alert('Erro: ' + data.error);
        }
    } catch (error) {
        alert('Erro na comunicação com o servidor: ' + error.message);
    }
});
