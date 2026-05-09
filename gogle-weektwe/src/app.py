from flask import Flask, request, jsonify, redirect, send_from_directory, abort
import os
from .service import URLService

# Flask will serve static files (css, images, index.html) from the project root
# `static_folder='.'` means the current working directory when the app is started
app = Flask(__name__, static_folder='.', static_url_path='')

# Shared URL service instance (in‑memory storage)
service = URLService()

# ---------------------------------------------------------------------
# Home page – serve the index.html that lives in the project root
# ---------------------------------------------------------------------
@app.route('/')
def serve_index():
    # ``os.getcwd()`` is the project root because we start the server from there
    return send_from_directory(os.getcwd(), 'index.html')

# ---------------------------------------------------------------------
# Generic static file route – needed for CSS, images, favicon, etc.
# Flask will also automatically serve files from ``static_folder`` but the
# explicit ``/<path:filename>`` route guarantees that files outside a "static"
# sub‑folder (e.g., css/style.css) are reachable.
# ---------------------------------------------------------------------
@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory(os.getcwd(), filename)

# ---------------------------------------------------------------------
# API – shorten a URL
# ---------------------------------------------------------------------
@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing "url" field'}), 400
    long_url = data['url']
    try:
        key = service.create_short(long_url)
        short_url = request.host_url + key
        return jsonify({'short_key': key, 'short_url': short_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ---------------------------------------------------------------------
# API – redirect short link to the original URL
# ---------------------------------------------------------------------
@app.route('/<key>')
def redirect_short(key):
    try:
        long_url = service.resolve(key)
        return redirect(long_url, code=302)
    except KeyError as e:
        abort(404, description=str(e))

# ---------------------------------------------------------------------
# API – stats for a short link
# ---------------------------------------------------------------------
@app.route('/stats/<key>', methods=['GET'])
def stats(key):
    try:
        return jsonify(service.stats(key))
    except KeyError as e:
        abort(404, description=str(e))

# ---------------------------------------------------------------------
# Run the development server
# ---------------------------------------------------------------------
if __name__ == '__main__':
    # ``host='0.0.0.0'`` makes the server reachable from any network
    app.run(host='0.0.0.0', port=5000, debug=True)
