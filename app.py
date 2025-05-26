from flask import Flask, request, send_from_directory, jsonify
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json() or request.form
    url = data.get('url')
    format_type = data.get('format', 'mp3')  # default mp3
    
    if not url:
        return jsonify({'error': 'URL não fornecida'}), 400
    
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
            'quiet': True,
        }
    elif format_type == 'mp4':
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'quiet': True,
        }
    else:
        return jsonify({'error': 'Formato inválido'}), 400
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if format_type == 'mp3':
                filename = filename.rsplit('.', 1)[0] + '.mp3'
            elif format_type == 'mp4':
                filename = filename.rsplit('.', 1)[0] + '.mp4'
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return send_from_directory(DOWNLOAD_FOLDER, os.path.basename(filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
