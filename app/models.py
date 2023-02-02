from app.app import db


class Users(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}


class Guests(db.Model):
    __tablename__ = 'guests'
    __table_args__ = {'extend_existing': True}


class Employees(db.Model):
    __tablename__ = 'employees'
    __table_args__ = {'extend_existing': True}


class Positions(db.Model):
    __tablename__ = 'positions'
    __table_args__ = {'extend_existing': True}


class Rooms(db.Model):
    __tablename__ = 'rooms'
    __table_args__ = {'extend_existing': True}


class RoomReservations(db.Model):
    __tablename__ = 'room_reservations'
    __table_args__ = {'extend_existing': True}


class Equipment(db.Model):
    __tablename__ = 'equipment'
    __table_args__ = {'extend_existing': True}


class EqCategories(db.Model):
    __tablename__ = 'eq_categories'
    __table_args__ = {'extend_existing': True}


class EqReservations(db.Model):
    __tablename__ = 'eq_reservations'
    __table_args__ = {'extend_existing': True}


class Tasks(db.Model):
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True}
