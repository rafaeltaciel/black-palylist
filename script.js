document.querySelector('button').addEventListener('click', () => {
  const url = document.querySelector('input[type="text"]').value.trim();
  if (!url) {
    alert('Por favor, cole um link válido!');
    return;
  }

  fetch('/download', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, format: 'mp3' })  // aqui você pode mudar para 'mp4' se quiser
  })
  .then(response => {
    if (!response.ok) throw new Error('Erro ao baixar o arquivo');
    return response.blob();
  })
  .then(blob => {
    // Cria um link para download automático do arquivo
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'playlist.mp3';  // ou .mp4, conforme o formato
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(link.href);
  })
  .catch(error => {
    alert('Erro: ' + error.message);
  });
});
