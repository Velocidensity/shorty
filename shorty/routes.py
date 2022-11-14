from io import BytesIO

import segno
import werkzeug.exceptions
from flask import Response, jsonify, redirect, render_template, request, url_for

from shorty import app
from shorty.db import URL
from shorty.helpers import validate_url


@app.route('/', methods=['GET'])
def front():
    return render_template('front.html')


@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html')


@app.route('/<string:stem>', methods=['GET'])
def redirect_stem(stem):
    if mapping := URL.get(stem):
        URL.hit(stem)
        return redirect(mapping.url)

    return render_template('404.html')


@app.route('/qr/<string:stem>.svg', methods=['GET'])
def qrcode_svg(stem):
    if mapping := URL.get(stem):
        svg = BytesIO()
        segno.make(mapping.stem).save(svg, scale=15, kind='svg', xmldecl=False)
        return Response(
            svg.getvalue().decode('utf-8'),
            mimetype='image/svg+xml',
        )

    return render_template('404.html')


@app.route('/qr/<string:stem>.png', methods=['GET'])
def qrcode_png(stem):
    if mapping := URL.get(stem):
        png = BytesIO()
        segno.make(mapping.stem).save(png, scale=15, kind='png')
        return Response(
            png.getvalue(),
            mimetype='image/png'
        )

    return render_template('404.html')


@app.route('/shorten', methods=['POST'])
def shorten():
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
        user_ip=request.remote_addr
    )

    return jsonify(
        stem=mapping.stem,
        url=url_for(
            'redirect_stem',
            stem=mapping.stem,
            _external=True
        )
    )
