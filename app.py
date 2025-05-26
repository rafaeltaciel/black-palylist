from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route('/download_playlist', methods=['POST'])
def download_playlist():
    data = request.get_json()
    playlist_url = data.get('url')
    
    if not playlist_url:
        return jsonify({'error': 'URL da playlist não fornecida'}), 400
    
    # Aqui você executa seu código para baixar com yt-dlp, por exemplo
    # E retorna resultado, status ou link para download
    
    # Exemplo dummy de resposta:
    return jsonify({'message': 'Download iniciado', 'url': playlist_url})

# Rota para servir index.html
@app.route('/')
def home():
    return send_from_directory('index.html')

# Rota para servir arquivos estáticos (JS, CSS, imagens, etc)
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory( filename)

if __name__ == '__main__':
    # Define pasta 'static' para arquivos estáticos
    # Certifique-se de que os arquivos index.html, style.css, script.js, logo.jpg estão dentro da pasta 'static'
    app.run(debug=True)
