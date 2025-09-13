from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get('url')

    # ---- INÍCIO DA LÓGICA DO YT-DLP ----

    # 1. Opções para o yt-dlp
    # Configuramos para extrair informações sem baixar o vídeo no servidor
    # e pedimos por formatos comuns.
    ydl_opts = {
        'noplaylist': True,
        'quiet': True,
        'format': 'best[ext=mp4]/best' # Pega o melhor formato MP4, ou o melhor disponível
    }

    try:
        # 2. Extraindo as informações
        # Aqui a mágica acontece. O yt-dlp "visita" a URL e pega tudo o que precisamos.
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)

            # 3. Preparando os dados para enviar de volta
            # Pegamos o título, a URL da miniatura e uma lista de formatos de vídeo.
            video_title = info_dict.get('title', 'Título não encontrado')
            thumbnail_url = info_dict.get('thumbnail', None)

            # Criamos uma lista para guardar os links de download
            formats = []
            for f in info_dict.get('formats', []):
                # Verificamos se o formato tem vídeo e áudio
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    formats.append({
                        'quality': f.get('format_note', f.get('resolution')),
                        'url': f.get('url'),
                        'ext': f.get('ext')
                    })

            # 4. Enviando a resposta completa para o JavaScript
            return jsonify({
                'success': True,
                'title': video_title,
                'thumbnail': thumbnail_url,
                'formats': formats
            })

    except Exception as e:
        # 5. Lidando com erros
        # Se a URL for inválida ou o vídeo não for encontrado, enviamos uma mensagem de erro.
        print(f"Erro ao processar a URL: {e}")
        return jsonify({'success': False, 'message': 'Não foi possível obter as informações do vídeo. Verifique o link.'})

    # ---- FIM DA LÓGICA DO YT-DLP ----

if __name__ == '__main__':
    app.run(debug=True)