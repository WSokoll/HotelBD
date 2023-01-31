from flask import Blueprint, render_template

bp = Blueprint('home', __name__, template_folder='templates')


# Show home page
# TODO login required
@bp.route('/home', methods=['GET'])
@bp.route('/', methods=['GET'])
def get():
    return render_template('home.jinja')
