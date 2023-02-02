from flask import Blueprint, flash, request, render_template, redirect, url_for, abort
from flask_login import login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length
from passlib.hash import sha256_crypt
from urllib.parse import urlparse, urljoin

from app.models import Users


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


bp = Blueprint('auth', __name__, template_folder='templates')


# Login page
@bp.route('/login', methods=['GET', 'POST'])
def login():

    class LoginForm(FlaskForm):
        login = StringField('Login', validators=[InputRequired(), Length(max=255)])
        password = StringField('Password', validators=[InputRequired(), Length(max=255)])

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(login=form.login.data).first()

        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)

        if user and sha256_crypt.verify(form.password.data, user.password):
            login_user(user)
            flash('Logged in successfully')

            return redirect(url_for('home.get_post'))
        else:
            flash('Invalid login details')
            return render_template('login.jinja', form=form)

    elif form.is_submitted():
        for field_name, errors in form.errors.items():
            for err in errors:
                flash(f"{form._fields[field_name].label.text}: {err}", 'error')

    return render_template('login.jinja', form=form)


# Logout
@bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home.get_post'))
