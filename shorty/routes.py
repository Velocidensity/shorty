from io import BytesIO

import segno
import werkzeug.exceptions
from flask import Response, jsonify, redirect, render_template, request, url_for

from shorty import app
from shorty.db import URL
from shorty.helpers import validate_url


@app.route('/', methods=['GET'])
def front():
    """Front page"""
    return render_template('front.html')


@app.route('/privacy', methods=['GET'])
def privacy():
    """Privacy policy page"""
    return render_template('privacy.html')


@app.route('/<string:stem>', methods=['GET'])
def redirect_stem(stem: str):
    """Redirect from stem"""
    if mapping := URL.get(stem):
        URL.hit(stem)
        return redirect(mapping.url)

    return render_template('404.html'), 404


@app.route('/stats/<string:stem>', methods=['GET'])
def redirect_stats(stem: str):
    """Alias for stem stats"""
    return redirect(url_for('stats', stem=stem))


@app.route('/<string:stem>+', methods=['GET'])
def stats(stem: str):
    """Stats page for a given stem"""
    if mapping := URL.get(stem):
        return render_template('stats.html', mapping=mapping)

    return render_template('404.html'), 404


@app.route('/qr/<string:stem>.svg', methods=['GET'])
def qrcode_svg(stem: str):
    """QR code for a given stem as SVG"""
    if mapping := URL.get(stem):
        svg = BytesIO()
        segno.make(mapping.stem).save(svg, scale=15, kind='svg', xmldecl=False)
        return Response(
            svg.getvalue().decode('utf-8'),
            mimetype='image/svg+xml',
        )

    return render_template('404.html'), 404


@app.route('/qr/<string:stem>.png', methods=['GET'])
def qrcode_png(stem: str):
    """QR code for a given stem as PNG"""
    if mapping := URL.get(stem):
        png = BytesIO()
        segno.make(mapping.stem).save(png, scale=15, kind='png')
        return Response(
            png.getvalue(),
            mimetype='image/png'
        )

    return render_template('404.html'), 404


@app.route('/api/info/<string:stem>', methods=['GET'])
def api(stem: str):
    """JSON API with info for a given stem"""
    if mapping := URL.get(stem):
        return jsonify(
            stem=mapping.stem,
            url=mapping.url,
            shortened_url=url_for(
                'redirect_stem',
                stem=mapping.stem,
                _external=True
            ),
            added_time=int(mapping.added_time.timestamp()),
            hits=mapping.hits
        )

    return render_template('404.html'), 404


@app.route('/api/shorten', methods=['POST'])
def shorten():
    """JSON API endpoint creating a shortened URL"""
    try:
        request.get_json(force=True, cache=True)
    except werkzeug.exceptions.BadRequest:
        return jsonify(error='Failed to parse input as JSON.'), 400

    if not request.json.get('url'):
        return jsonify(error='URL to shorten not provided.'), 400

    if not validate_url(request.json['url']):
        return jsonify(error='Invalid URL provided.'), 400

    mapping = URL.add(
        url=request.json['url'],
        user_ip=request.remote_addr,
        force=request.json.get('force', False)
    )

    return jsonify(
        stem=mapping.stem,
        shortened_url=url_for(
            'redirect_stem',
            stem=mapping.stem,
            _external=True
        )
    )
