from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()


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

    # Init flask login
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.models import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.filter_by(id=int(user_id)).first()

    # Register blueprints
    from app.views.home import bp as bp_home
    app.register_blueprint(bp_home)

    from app.views.auth import bp as bp_auth
    app.register_blueprint(bp_auth)

    from app.views.guest_personal import bp as bp_guest_personal
    app.register_blueprint(bp_guest_personal)

    from app.views.room_reservation import bp as bp_room_reservation
    app.register_blueprint(bp_room_reservation)

    from app.views.eq_reservation import bp as bp_eq_reservation
    app.register_blueprint(bp_eq_reservation)

    return app
