from flask import Blueprint, render_template, abort, flash
from flask_login import current_user
from sqlalchemy import and_

from app.app import db
from app.forms.guest import GuestPersonalForm, RoomReservationForm, EquipmentReservationForm
from app.models import Guests, Rooms, RoomReservations, EqCategories, Equipment, EqReservations

bp = Blueprint('home', __name__, template_folder='templates')


# TODO login required
@bp.route('/home', methods=['GET', 'POST'])
@bp.route('/', methods=['GET', 'POST'])
def get_post():
    if current_user.is_authenticated and current_user.guest_id is not None:

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
                )).all()

                if reservations:
                    reserved = True

            if not room:
                flash('Invalid room number.')
            elif room_res_form.num_of_people > room.capacity:
                flash('Number of people exceeds room capacity.')
            elif reserved:
                flash('Room not available on the selected dates.')
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
                room_res_form = RoomReservationForm()

        elif room_res_form.is_submitted():
            for field_name, errors in room_res_form.errors.items():
                for err in errors:
                    flash(f"{room_res_form._fields[field_name].label.text}: {err}", 'error')

        eq_categories = EqCategories.query.order_by(EqCategories.name).all()
        eq_res_form = EquipmentReservationForm()
        eq_res_form.eq_category.choices = [eq.name for eq in eq_categories]

        if eq_res_form.validate_on_submit():
            # check other reservations
            eq = Equipment.query.filter_by(name=eq_res_form.eq_name.data).one_or_none()
            reserved = False
            if eq:
                reservations = EqReservations.query.filter(and_(
                    EqReservations.equipment_id == eq.id,
                    and_(
                        EqReservations.start_date < eq_res_form.end_date.data,
                        EqReservations.end_date > eq_res_form.start_date.data
                    )
                )).all()

                if reservations:
                    reserved = True

            if not eq:
                flash('Invalid equipment name.')
            elif reserved:
                flash('Equipment not available on the selected dates.')
            else:
                eq_reservation = EqReservations(
                    equipment_id=eq.id,
                    guest_id=current_user.id,
                    start_date=eq_res_form.start_date.data,
                    end_date=eq_res_form.end_date.data
                )
                db.session.add(eq_reservation)
                db.session.commit()

                flash('Reservation added.')
                eq_res_form = EquipmentReservationForm()

        elif eq_res_form.is_submitted():
            for field_name, errors in eq_res_form.errors.items():
                for err in errors:
                    flash(f"{eq_res_form._fields[field_name].label.text}: {err}", 'error')

        return render_template('home.jinja',
                               rooms=rooms,
                               guest_personal_form=guest_personal_form,
                               room_res_form=room_res_form,
                               eq_res_form=eq_res_form)

    elif current_user.is_authenticated and current_user.employee_id is not None:
        pass

    return render_template('home.jinja')
