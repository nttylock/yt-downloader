import sys
import os
import site
site.main()

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from yt_extractor import get_video_info, get_audio_and_video_urls
from urllib.parse import urlparse, parse_qs, urlencode

app = Flask(__name__)
CORS(app)  # This will allow requests from any source

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        # Clean URL from playlist parameters
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params.pop('list', None)
        clean_url = parsed_url._replace(query=urlencode(query_params, doseq=True)).geturl()
        
        video_info = get_video_info(clean_url)
        if video_info:
            audio_url, video_url, video_ext, video_size, audio_size, video_resolution = get_audio_and_video_urls(video_info)
            return jsonify({
                'audio_url': audio_url,
                'audio_size': audio_size,
                'video_url': video_url,
                'video_ext': video_ext,
                'video_size': video_size,
                'video_resolution': video_resolution
            })
        else:
            return jsonify({'error': 'Failed to get video information'})
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)