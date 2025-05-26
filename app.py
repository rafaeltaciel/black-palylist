from flask import Flask, send_from_directory

app = Flask(__name__)

# Rota raiz, serve seu index.html
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Rota para arquivos estáticos (css, js, imagens)
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True)
