import os
import uuid
import yt_dlp
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download():

    video_url = request.args.get("url")
    format_option = request.args.get("format", "video").lower()

    if not video_url:
        return jsonify({"error": "O parâmetro 'url' é obrigatório."}), 400

    random_id = uuid.uuid4().hex
    outtmpl = f"/tmp/{random_id}_%(title)s.%(ext)s"

    ydl_opts = {
        'outtmpl': outtmpl,
        'quiet': True,
    }
    if format_option == "audio":
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            if format_option == "audio":
              
                filename = os.path.splitext(filename)[0] + ".mp3"
    except Exception as e:
        return jsonify({"error": f"Erro ao baixar o vídeo/áudio: {str(e)}"}), 500

    if not os.path.exists(filename):
        return jsonify({"error": "Falha ao gerar o arquivo."}), 500

    try:

        response = send_file(filename, as_attachment=True, download_name=os.path.basename(filename))

        response.call_on_close(lambda: os.remove(filename))
        return response
    except Exception as e:
        if os.path.exists(filename):
            os.remove(filename)
        return jsonify({"error": f"Erro ao enviar o arquivo: {str(e)}"}), 500

def app_main(request):
    return app(request)
