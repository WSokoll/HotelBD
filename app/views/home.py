from flask import Blueprint, render_template, abort, flash
from flask_login import current_user
from sqlalchemy import and_

from app.app import db
from app.forms.guest import GuestPersonalForm, RoomReservationForm, EquipmentReservationForm
from app.models import Guests, Rooms, RoomReservations, EqCategories, Equipment, EqReservations

bp = Blueprint('home', __name__, template_folder='templates')


@bp.route('/home', methods=['GET'])
@bp.route('/', methods=['GET'])
def get():
    return render_template('home.jinja')
