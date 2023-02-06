from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink

import app.models


class EmployeesModelView(ModelView):
    can_view_details = True
    can_create = True
    can_edit = True
    can_delete = True
    column_list = [
        'first_name', 'last_name', 'position_id'
    ]
    column_details_list = [
        'id', 'first_name', 'last_name', 'position_id', 'tel_number', 'email'
    ]
    form_columns = [
        'first_name', 'last_name', 'position_id', 'tel_number', 'email'
    ]


class TasksModelView(ModelView):
    can_view_details = True
    can_create = True
    can_edit = True
    can_delete = True
    column_list = [
        'room_id', 'name'
    ]
    column_details_list = [
        'id', 'room_id', 'name', 'employee_id', 'description'
    ]
    form_columns = [
        'room_id', 'name', 'employee_id', 'description'
    ]


class RoomsModelView(ModelView):
    can_view_details = True
    can_create = True
    can_edit = True
    can_delete = True
    column_list = [
        'number', 'capacity', 'price_per_day'
    ]
    column_details_list = [
        'id', 'number', 'description', 'capacity', 'price_per_day'
    ]
    form_columns = [
        'number', 'description', 'capacity', 'price_per_day'
    ]


class RoomReservationsModelView(ModelView):
    can_view_details = True
    can_create = True
    can_edit = True
    can_delete = True
    column_list = [
        'room_id', 'start_date', 'end_date', 'num_of_people'
    ]
    column_details_list = [
        'id', 'room_id', 'start_date', 'end_date', 'num_of_people', 'guest_id'
    ]
    form_columns = [
        'room_id', 'start_date', 'end_date', 'num_of_people', 'guest_id'
    ]


class EquipmentModelView(ModelView):
    can_view_details = True
    can_create = True
    can_edit = True
    can_delete = True
    column_list = [
        'cat_id', 'name', 'cost_per_hour'
    ]
    column_details_list = [
        'id', 'cat_id', 'name', 'description', 'cost_per_hour'
    ]
    form_columns = [
        'cat_id', 'name', 'description', 'cost_per_hour'
    ]


class EqReservationsModelView(ModelView):
    can_view_details = True
    can_create = True
    can_edit = True
    can_delete = True
    column_list = [
        'equipment_id', 'start_date', 'end_date'
    ]
    column_details_list = [
        'id', 'equipment_id', 'start_date', 'end_date', 'guest_id'
    ]
    form_columns = [
        'equipment_id', 'start_date', 'end_date', 'guest_id'
    ]


def admin_panel_init(admin, db):

    class LogoutLink(MenuLink):
        def get_url(self):
            return url_for("auth.logout")

    class HomePageLink(MenuLink):
        def get_url(self):
            return url_for("home.get")

    admin.add_link(LogoutLink(name="Log out"))
    admin.add_link(HomePageLink(name="Home"))

    admin.add_view(EmployeesModelView(app.models.Employees, db.session, name='Employees'))
    admin.add_view(TasksModelView(app.models.Tasks, db.session, name='Tasks'))
    admin.add_view(RoomsModelView(app.models.Rooms, db.session, name='Rooms'))
    admin.add_view(RoomReservationsModelView(app.models.RoomReservations, db.session, name='R.Reservations'))
    admin.add_view(EquipmentModelView(app.models.Equipment, db.session, name='Equipment'))
    admin.add_view(EqReservationsModelView(app.models.EqReservations, db.session, name='E.Reservations'))
