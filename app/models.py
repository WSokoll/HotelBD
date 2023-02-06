from flask_login import UserMixin

from app.app import db


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        return self.login


class Guests(db.Model):
    __tablename__ = 'guests'
    __table_args__ = {'extend_existing': True}


class Positions(db.Model):
    __tablename__ = 'positions'
    __table_args__ = {'extend_existing': True}


class Employees(db.Model):
    __tablename__ = 'employees'
    __table_args__ = {'extend_existing': True}

    position = db.relationship('Positions', foreign_keys='Employees.position_id')


class Rooms(db.Model):
    __tablename__ = 'rooms'
    __table_args__ = {'extend_existing': True}


class RoomReservations(db.Model):
    __tablename__ = 'room_reservations'
    __table_args__ = {'extend_existing': True}

    room = db.relationship('Rooms', foreign_keys='RoomReservations.room_id')


class EqCategories(db.Model):
    __tablename__ = 'eq_categories'
    __table_args__ = {'extend_existing': True}


class Equipment(db.Model):
    __tablename__ = 'equipment'
    __table_args__ = {'extend_existing': True}

    category = db.relationship('EqCategories', foreign_keys='Equipment.cat_id')


class EqReservations(db.Model):
    __tablename__ = 'eq_reservations'
    __table_args__ = {'extend_existing': True}

    equipment = db.relationship('Equipment', foreign_keys='EqReservations.equipment_id')


class Tasks(db.Model):
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True}

    room = db.relationship('Rooms', foreign_keys='Tasks.room_id')
