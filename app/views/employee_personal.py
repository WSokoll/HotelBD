from flask import Blueprint, abort, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from app.app import db
from app.forms.employee import EmployeePersonalForm
from app.models import Employees, Positions

bp = Blueprint('employee_personal', __name__, template_folder='templates')


@bp.route('/employee/personal', methods=['GET', 'POST'])
@login_required
def get_post():
    if not current_user.is_authenticated or current_user.employee_id is None:
        abort(401)

    employee = Employees.query.filter_by(id=current_user.employee_id).one_or_none()
    if not employee:
        abort(400)

    position = Positions.query.filter_by(id=employee.position_id).one_or_none()
    if not position:
        abort(400)

    employee_personal_form = EmployeePersonalForm()

    if employee_personal_form.validate_on_submit():
        employee.first_name = employee_personal_form.first_name.data
        employee.last_name = employee_personal_form.last_name.data
        employee.tel_number = employee_personal_form.tel_number.data
        employee.email = employee_personal_form.email.data

        db.session.commit()
        flash('Personal information has been successfully updated.')

    elif employee_personal_form.is_submitted():
        for field_name, errors in employee_personal_form.errors.items():
            for err in errors:
                flash(f"{employee_personal_form._fields[field_name].label.text}: {err}", 'error')

        return render_template('employee_personal.jinja', employee_personal_form=employee_personal_form)

    employee_personal_form.first_name.data = employee.first_name
    employee_personal_form.last_name.data = employee.last_name
    employee_personal_form.tel_number.data = employee.tel_number
    employee_personal_form.email.data = employee.email
    employee_personal_form.position.data = position.name

    return render_template('employee_personal.jinja', employee_personal_form=employee_personal_form)
