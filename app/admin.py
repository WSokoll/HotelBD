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
        'first_name', 'last_name', 'position.name'
    ]
    column_details_list = [
        'id', 'first_name', 'last_name', 'position_id', 'position.name', 'tel_number', 'email'
    ]
    form_columns = [
        'first_name', 'last_name', 'position_id', 'tel_number', 'email'
    ]
    column_labels = {
        'position.name': 'Position Name'
    }


class TasksModelView(ModelView):
    can_view_details = True
    can_create = True
    can_edit = True
    can_delete = True
    column_list = [
        'room.number', 'name'
    ]
    column_details_list = [
        'id', 'room_id', 'room.number', 'name', 'employee_id', 'description'
    ]
    form_columns = [
        'room_id', 'name', 'employee_id', 'description'
    ]
    column_labels = {
        'room.number': 'Room Number'
    }


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
        'room.number', 'start_date', 'end_date', 'num_of_people'
    ]
    column_details_list = [
        'id', 'room_id', 'room.number',  'start_date', 'end_date', 'num_of_people', 'guest_id'
    ]
    form_columns = [
        'room_id', 'start_date', 'end_date', 'num_of_people', 'guest_id'
    ]
    column_labels = {
        'room.number': 'Room Number'
    }


class EquipmentModelView(ModelView):
    can_view_details = True
    can_create = True
    can_edit = True
    can_delete = True
    column_list = [
        'category.name', 'name', 'cost_per_hour'
    ]
    column_details_list = [
        'id', 'category.name', 'cat_id', 'name', 'description', 'cost_per_hour'
    ]
    form_columns = [
        'cat_id', 'name', 'description', 'cost_per_hour'
    ]
    column_labels = {
        'category.name': 'Category'
    }


class EqReservationsModelView(ModelView):
    can_view_details = True
    can_create = True
    can_edit = True
    can_delete = True
    column_list = [
        'equipment.name', 'start_date', 'end_date'
    ]
    column_details_list = [
        'id', 'equipment_id', 'equipment.name', 'start_date', 'end_date', 'guest_id'
    ]
    form_columns = [
        'equipment_id', 'start_date', 'end_date', 'guest_id'
    ]
    column_labels = {
        'equipment.name': 'Equipment'
    }


class GuestsModelView(ModelView):
    can_view_details = True
    can_create = False
    can_edit = True
    can_delete = True
    column_list = [
        'first_name', 'last_name', 'email'
    ]
    column_details_list = [
        'id', 'first_name', 'last_name', 'email', 'age', 'tel_number'
    ]
    form_columns = [
        'first_name', 'last_name', 'email', 'age', 'tel_number'
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
    admin.add_view(GuestsModelView(app.models.Guests, db.session, name='Guests'))
    admin.add_view(RoomsModelView(app.models.Rooms, db.session, name='Rooms'))
    admin.add_view(RoomReservationsModelView(app.models.RoomReservations, db.session, name='R.Reservations'))
    admin.add_view(EquipmentModelView(app.models.Equipment, db.session, name='Equipment'))
    admin.add_view(EqReservationsModelView(app.models.EqReservations, db.session, name='E.Reservations'))
