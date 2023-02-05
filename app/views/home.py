from datetime import datetime

from flask import Blueprint, render_template
from flask_login import current_user

from app.models import RoomReservations, Rooms, EqReservations, Equipment, Tasks

bp = Blueprint('home', __name__, template_folder='templates')


@bp.route('/home', methods=['GET'])
@bp.route('/', methods=['GET'])
def get():

    if current_user.is_authenticated and current_user.guest_id is not None:
        room_res = RoomReservations.query.filter_by(guest_id=current_user.id).all()
        room_res_list = []

        for res in room_res:
            room = Rooms.query.filter_by(id=res.room_id).first()

            res_element = {
                'room_number': room.number,
                'start_date': datetime.strftime(res.start_date, '%Y-%m-%d'),
                'end_date': datetime.strftime(res.end_date, '%Y-%m-%d'),
                'num_of_people': res.num_of_people,
                'price': room.price_per_day * (res.end_date - res.start_date).days
            }
            room_res_list.append(res_element)

        eq_res = EqReservations.query.filter_by(guest_id=current_user.id).all()
        eq_res_list = []

        for res in eq_res:
            equipment = Equipment.query.filter_by(id=res.equipment_id).first()

            res_element = {
                'equipment': equipment.name,
                'start_date': datetime.strftime(res.start_date, '%Y-%m-%d'),
                'end_date': datetime.strftime(res.end_date, '%Y-%m-%d'),
                'price': equipment.cost_per_hour * (res.end_date - res.start_date).days * 24
            }
            eq_res_list.append(res_element)

        return render_template('home.jinja', room_res_list=room_res_list, eq_res_list=eq_res_list)

    elif current_user.is_authenticated and current_user.employee_id is not None:
        tasks = Tasks.query.filter_by(employee_id=current_user.employee_id).all()
        list_of_tasks = []

        for task in tasks:
            room = Rooms.query.filter_by(id=task.room_id).first()

            task_element = {
                'room_number': room.number,
                'name': task.name,
                'description': task.description
            }
            list_of_tasks.append(task_element)

        return render_template('home.jinja', tasks=list_of_tasks)

    return render_template('home.jinja')
