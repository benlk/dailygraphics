#!/usr/bin/env python

import argparse
from glob import glob

from flask import Flask, render_template

import app_config
from render_utils import make_context, urlencode_filter
import static

app = Flask(app_config.PROJECT_NAME)

app.jinja_env.filters['urlencode'] = urlencode_filter

@app.route('/')
def _graphics_list():
    context = make_context()
    context['graphics'] = []

    graphics = glob('www/graphics/*/child.html')
    for graphic in graphics:
        context['graphics'].append(graphic.split('www/graphics/')[1].split('/child.html')[0])

    context['graphics_count'] = len(context['graphics'])

    return render_template('index.html', **context)

@app.route('/graphics/<slug>/')
def _graphics_detail(slug):
    """
    Renders a parent.html index with child.html embedded as iframe.
    """

    context = make_context()
    context['slug'] = slug
    context['domain'] = app_config.S3_BASE_URL
    context['xdomain'] = None 

    if app_config.DEPLOYMENT_TARGET:
        context['xdomain'] = 'npr.org'

    return render_template('parent.html', **context)

app.register_blueprint(static.static)

# Boilerplate
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port')
    args = parser.parse_args()
    server_port = 8000

    if args.port:
        server_port = int(args.port)

    app.run(host='0.0.0.0', port=server_port, debug=app_config.DEBUG)
