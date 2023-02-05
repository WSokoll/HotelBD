from flask import Flask, abort, redirect, url_for
from flask_admin import AdminIndexView, Admin
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy


class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if not current_user.is_active and not current_user.is_authenticated:
            return False

        if not current_user.employee_id:
            return False

        from app.models import Employees
        employee = Employees.query.filter_by(id=current_user.employee_id).one_or_none()

        if employee and (employee.position_id == 1 or employee.position_id == 2):
            return True
        else:
            return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('auth.login'))


db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin(name='Admin - HotelBD', template_mode='bootstrap4', index_view=CustomAdminIndexView())


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

    # Admin
    admin.init_app(app)

    from app.admin import admin_panel_init
    admin_panel_init(admin, db)

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

    from app.views.employee_personal import bp as bp_employee_personal
    app.register_blueprint(bp_employee_personal)

    return app
