from flask import Blueprint, render_template
from flask_login import current_user

bp = Blueprint('home', __name__, template_folder='templates')


# TODO login required
@bp.route('/home', methods=['GET', 'POST'])
@bp.route('/', methods=['GET', 'POST'])
def get_post():

    if current_user.guest_id is not None:
        pass

    elif current_user.employee_id is not None:
        pass

    return render_template('home.jinja')
