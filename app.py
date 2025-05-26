from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL não fornecida'}), 400

    ydl_opts = {
        'outtmpl': 'downloads/%(playlist_index)s - %(title)s.%(ext)s',
        'ignoreerrors': True,
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({'message': 'Download concluído com sucesso!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
