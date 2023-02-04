from flask import Blueprint, abort, flash, render_template
from flask_login import login_required, current_user

from app.app import db
from app.forms.guest import GuestPersonalForm
from app.models import Guests

bp = Blueprint('guest_personal', __name__, template_folder='templates')


@bp.route('/guest/personal', methods=['GET', 'POST'])
@login_required
def get_post():
    if not current_user.is_authenticated or current_user.guest_id is None:
        abort(401)

    guest = Guests.query.filter_by(id=current_user.guest_id).one_or_none()
    if not guest:
        abort(400)

    guest_personal_form = GuestPersonalForm()

    guest_personal_form.first_name.data = guest.first_name
    guest_personal_form.last_name.data = guest.last_name
    guest_personal_form.age.data = guest.age
    guest_personal_form.tel_number.data = guest.tel_number
    guest_personal_form.email.data = guest.email

    if guest_personal_form.validate_on_submit():
        guest.first_name = guest_personal_form.first_name.data
        guest.last_name = guest_personal_form.last_name.data
        guest.age = guest_personal_form.age.data
        guest.tel_number = guest_personal_form.tel_number.data
        guest.email = guest_personal_form.email.data

        db.session.commit()
        flash('Personal information has been successfully updated.')

    elif guest_personal_form.is_submitted():
        for field_name, errors in guest_personal_form.errors.items():
            for err in errors:
                flash(f"{guest_personal_form._fields[field_name].label.text}: {err}", 'error')

    return render_template('guest_personal.jinja', guest_personal_form=guest_personal_form)
