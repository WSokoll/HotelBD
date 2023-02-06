from flask import Blueprint, abort, flash, render_template, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import and_

from app.app import db
from app.forms.guest import RoomReservationForm
from app.models import Rooms, RoomReservations

bp = Blueprint('room_reservation', __name__, template_folder='templates')


@bp.route('/guest/room/reservation', methods=['GET', 'POST'])
@login_required
def get_post():
    if not current_user.is_authenticated or current_user.guest_id is None:
        abort(401)

    rooms = Rooms.query.order_by(Rooms.id).all()

    room_res_form = RoomReservationForm()
    room_res_form.room_number.choices = [room.number for room in rooms]

    if room_res_form.validate_on_submit():
        # check other reservations
        room = Rooms.query.filter_by(number=room_res_form.room_number.data).one_or_none()
        reserved = False
        if room:
            reservations = RoomReservations.query.filter(and_(
                RoomReservations.room_id == room.id,
                and_(
                    RoomReservations.start_date < room_res_form.end_date.data,
                    RoomReservations.end_date > room_res_form.start_date.data
                )
            )).count()

            if reservations > 0:
                reserved = True

        if not room:
            flash('Invalid room number.', 'error')
        elif room_res_form.num_of_people.data > room.capacity:
            flash('Number of people exceeds room capacity.', 'error')
        elif reserved:
            flash('Room not available on the selected dates.', 'error')
        else:
            room_reservation = RoomReservations(
                guest_id=current_user.id,
                room_id=room.id,
                start_date=room_res_form.start_date.data,
                end_date=room_res_form.end_date.data,
                num_of_people=room_res_form.num_of_people.data
            )
            db.session.add(room_reservation)
            db.session.commit()

            flash('Reservation added.')
            return redirect(url_for('room_reservation.get_post'))

    elif room_res_form.is_submitted():
        for field_name, errors in room_res_form.errors.items():
            for err in errors:
                flash(f"{room_res_form._fields[field_name].label.text}: {err}", 'error')

    return render_template('room_reservation.jinja', rooms=rooms, room_res_form=room_res_form)
