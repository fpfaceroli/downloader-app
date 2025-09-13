# Importamos uma nova ferramenta, "send_from_directory"
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import yt_dlp
import os # Importamos o 'os' para lidar com caminhos de arquivos

# A configuração agora aponta para a pasta onde está nosso index.html
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# --- ROTA NOVA PARA A PÁGINA PRINCIPAL ---
# Esta função será executada quando alguém acessar a URL raiz (ex: seudominio.com/)
@app.route('/')
def serve_index():
    # A função envia o arquivo 'index.html' da nossa pasta como resposta
    return send_from_directory('.', 'index.html')

# --- NOSSA ROTA DE DOWNLOAD EXISTENTE ---
@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get('url')

    ydl_opts = {
        'noplaylist': True,
        'quiet': True,
        'format': 'best[ext=mp4]/best'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)

            video_title = info_dict.get('title', 'Título não encontrado')
            thumbnail_url = info_dict.get('thumbnail', None)
            
            formats = []
            for f in info_dict.get('formats', []):
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    formats.append({
                        'quality': f.get('format_note', f.get('resolution')),
                        'url': f.get('url'),
                        'ext': f.get('ext')
                    })
            
            return jsonify({
                'success': True,
                'title': video_title,
                'thumbnail': thumbnail_url,
                'formats': formats
            })

    except Exception as e:
        print(f"Erro ao processar a URL: {e}")
        return jsonify({'success': False, 'message': 'Não foi possível obter as informações do vídeo. Verifique o link.'})

if __name__ == '__main__':
    app.run(debug=True)