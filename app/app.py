from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=False,
        static_folder='static',
        static_url_path='/static'
    )

    app.config.from_pyfile('config.default.py')
    app.config.from_pyfile('../local/config.local.py')

    app.config['SQLALCHEMY_DATABASE_URI'] = (f"postgresql://{app.config['DB_USER']}:{app.config['DB_PASSWORD']}"
                                             f"@{app.config['DB_HOST']}:{app.config['DB_PORT']}"
                                             f"/{app.config['DB_NAME']}")

    db.init_app(app)

    with app.app_context():
        db.reflect()

    # Register blueprints
    from app.views.home import bp as bp_home
    app.register_blueprint(bp_home)

    return app
