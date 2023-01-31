from flask import Flask


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=False,
        static_folder='static',
        static_url_path='/static'
    )

    app.config.from_pyfile('config.default.py')
    app.config.from_pyfile('../local/config.local.py')

    # Register blueprints
    from app.views.home import bp as bp_home
    app.register_blueprint(bp_home)

    return app