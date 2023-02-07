import datetime

from flask import Blueprint, abort, flash, render_template, redirect, url_for, jsonify
from flask_login import current_user, login_required
from sqlalchemy import and_

from app.app import db
from app.forms.guest import EquipmentReservationForm
from app.models import EqCategories, Equipment, EqReservations

bp = Blueprint('eq_reservation', __name__, template_folder='templates')


@bp.route('/guest/equipment/reservation', methods=['GET', 'POST'])
@login_required
def get_post():
    if not current_user.is_authenticated or current_user.guest_id is None:
        abort(401)

    eq_res_form = EquipmentReservationForm()

    eq_categories = EqCategories.query.order_by(EqCategories.name).all()
    eq_res_form.eq_category.choices = [cat.name for cat in eq_categories]

    eq_list = Equipment.query.order_by(Equipment.name).all()
    eq_res_form.eq_name.choices = [eq.name for eq in eq_list]

    if eq_res_form.validate_on_submit():
        # Merge date and hour
        start_date = eq_res_form.start_date.data
        start_hour = eq_res_form.start_date_hour.data
        end_date = eq_res_form.end_date.data
        end_hour = eq_res_form.end_date_hour.data

        start = datetime.datetime.combine(start_date, start_hour)
        end = datetime.datetime.combine(end_date, end_hour)

        start = start - datetime.timedelta(minutes=start_hour.minute)

        if end_hour.minute != 0:
            if end_hour.hour == 23:
                end = end - datetime.timedelta(hours=end_hour.hour, minutes=end_hour.minute)
                end = end + datetime.timedelta(days=1)
            else:
                end = end + datetime.timedelta(minutes=(60 - end_hour.minute))

        # check other reservations
        eq = Equipment.query.filter_by(name=eq_res_form.eq_name.data).one_or_none()
        reserved = False
        if eq:
            reservations = EqReservations.query.filter(and_(
                EqReservations.equipment_id == eq.id,
                and_(
                    EqReservations.start_date < end,
                    EqReservations.end_date > start
                )
            )).count()

            if reservations > 0:
                reserved = True

        if not eq:
            flash('Invalid equipment name.', 'error')
        elif reserved:
            flash('Equipment not available on the selected dates.', 'error')
        else:
            eq_reservation = EqReservations(
                equipment_id=eq.id,
                guest_id=current_user.id,
                start_date=start,
                end_date=end
            )
            db.session.add(eq_reservation)
            db.session.commit()

            flash('Reservation added.')
            return redirect(url_for('eq_reservation.get_post'))

    elif eq_res_form.is_submitted():
        for field_name, errors in eq_res_form.errors.items():
            for err in errors:
                flash(f"{eq_res_form._fields[field_name].label.text}: {err}", 'error')

    return render_template('eq_reservation.jinja', eq_res_form=eq_res_form)


@bp.route('/equipment/<string:category_name>')
@login_required
def equipment(category_name: str):
    category = EqCategories.query.filter_by(name=category_name.replace('%20', ' ').capitalize()).one_or_none()

    if not category:
        abort(400)

    equipment = Equipment.query.filter_by(cat_id=category.id).all()
    return jsonify({'equipment_list': [eq.name for eq in equipment]})
