from flask import Flask, request, send_from_directory, jsonify
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/download', methods=['POST'])
def download():
    # Pega JSON ou form data
    data = request.get_json(silent=True) or request.form
    url = data.get('url')
    format_type = data.get('format', 'mp3').lower()

    if not url:
        return jsonify({'error': 'URL não fornecida'}), 400

    if format_type not in ['mp3', 'mp4']:
        return jsonify({'error': 'Formato inválido. Use "mp3" ou "mp4".'}), 400

    ydl_opts = {}

    if format_type == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }
    else:  # mp4
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # Ajusta extensão para o formato correto
            base, _ = os.path.splitext(filename)
            filename = base + ('.mp3' if format_type == 'mp3' else '.mp4')
    except Exception as e:
        return jsonify({'error': f'Falha ao baixar: {str(e)}'}), 500

    # Retorna o arquivo para download
    return send_from_directory(DOWNLOAD_FOLDER, os.path.basename(filename), as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
