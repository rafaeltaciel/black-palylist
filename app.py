from flask import Flask, render_template_string, request, send_from_directory
import yt_dlp
import os
import base64

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Carregue seu logo.png e converta para base64
with open("logo.jpg", "rb") as image_file:
    logo_base64 = base64.b64encode(image_file.read()).decode('utf-8')

html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Black Playlist - Downloader</title>
    <style>
        /* Seu CSS aqui embutido */
        body {{
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 0;
            background: #121212;
            color: #fff;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #000;
            padding: 10px 20px;
        }}
        .logo-container {{
            display: flex;
            align-items: center;
        }}
        .logo {{
            height: 40px;
            margin-right: 10px;
        }}
        nav.menu a {{
            margin-left: 15px;
            color: #fff;
            text-decoration: none;
        }}
        main {{
            padding: 20px;
        }}
        input[type="text"] {{
            width: 80%;
            padding: 8px;
            margin-bottom: 10px;
            border-radius: 4px;
            border: none;
        }}
        button {{
            padding: 8px 16px;
            background: #1db954;
            color: #fff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }}
        footer {{
            text-align: center;
            padding: 15px;
            background: #000;
            margin-top: 20px;
        }}
    </style>
</head>
<body>

<header class="header">
    <div class="logo-container">
        <img src="data:image/png;base64,{logo_base64}" alt="Logo" class="logo" />
        <h1>Black Playlist</h1>
    </div>
    <nav class="menu">
        <a href="#download">Download</a>
        <a href="#instrucoes">Instruções</a>
        <a href="#faq">FAQ</a>
        <a href="#contato">Contato</a>
    </nav>
</header>

<main>
    <section id="download">
        <h2>Baixar Playlist</h2>
        <p>Cole o link da sua playlist do YouTube abaixo para baixar.</p>
        <form method="POST" action="/download">
            <input type="text" name="url" placeholder="Cole o link aqui..." required />
            <br/><br/>
            <label><input type="radio" name="format" value="mp3" checked> MP3</label>
            <label><input type="radio" name="format" value="mp4"> MP4</label>
            <br/><br/>
            <button type="submit">Baixar</button>
        </form>
    </section>

    <section id="instrucoes">
        <h2>Instruções</h2>
        <ul>
            <li>Copie o link da playlist do YouTube.</li>
            <li>Cole no campo acima.</li>
            <li>Clique em "Baixar".</li>
        </ul>
    </section>

    <section id="faq">
        <h2>FAQ</h2>
        <p><strong>O download é gratuito?</strong> Sim.</p>
        <p><strong>Posso baixar playlists inteiras?</strong> Sim, esse é o foco do site.</p>
    </section>

    <section id="contato">
        <h2>Contato</h2>
        <p>Email: <a href="mailto:contato@blackplaylist.com">contato@blackplaylist.com</a></p>
    </section>
</main>

<footer>
    &copy; 2025 Black Playlist. Todos os direitos reservados.
</footer>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_type = request.form['format']  # 'mp3' ou 'mp4'

    ydl_opts = {}
    if format_type == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    elif format_type == 'mp4':
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if format_type == 'mp3':
            filename = filename.rsplit('.', 1)[0] + '.mp3'
        elif format_type == 'mp4':
            filename = filename.rsplit('.', 1)[0] + '.mp4'

    return send_from_directory(DOWNLOAD_FOLDER, os.path.basename(filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
