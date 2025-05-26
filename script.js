document.querySelector('#download button').addEventListener('click', async () => {
  const input = document.querySelector('#download input');
  const url = input.value.trim();
  if (!url) {
    alert('Por favor, cole o link da playlist.');
    return;
  }

  try {
    const response = await fetch('/download', { // endpoint do seu backend
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });

    const data = await response.json();

    if (response.ok) {
      alert('Download iniciado! ' + (data.message || ''));
    } else {
      alert('Erro: ' + (data.error || 'Erro desconhecido'));
    }
  } catch (err) {
    alert('Erro na comunicação com o servidor: ' + err.message);
  }
});
