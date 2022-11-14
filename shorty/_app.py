import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask('shorty')
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_prefix=1, x_proto=1)

app.config.from_pyfile('default.cfg')
if os.environ.get('SHORTY_CONFIG'):
    app.config.from_envvar('SHORTY_CONFIG')

with app.app_context():
    db = SQLAlchemy(app)
    import shorty.db  # isort: skip # noqa: F401
    Migrate(app, db)
    db.create_all()
