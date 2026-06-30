from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app) # Crucial: This lets your WordPress site talk to this API

@app.route('/api/playlist', methods=['POST'])
def get_playlist_videos():
    data = request.json
    playlist_url = data.get('url')

    if not playlist_url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'extract_flat': True,  
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)

            if 'entries' not in playlist_info:
                return jsonify({"error": "Not a valid playlist"}), 400

            videos = []
            for entry in playlist_info['entries']:
                if entry: 
                    videos.append({
                        'title': entry.get('title'),
                        'url': f"https://www.youtube.com/watch?v={entry.get('id')}"
                    })

            return jsonify({
                'playlist_title': playlist_info.get('title'),
                'videos': videos
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
