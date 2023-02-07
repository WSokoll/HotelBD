from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, DateField, TimeField
from wtforms.validators import InputRequired, Length, Regexp, Email, NumberRange

from app.validators import AfterStartValidator, NotPastValidator

LETTERS_REGEXP = r'^[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+$'
PH_NUM_MESS = 'Number should look like YYXXXXXXXXX,' \
              ' where YYYY is the dialing code e.g. 48 for Poland, and X’s are the digits of phone number'


# Guest's personal data form
class GuestPersonalForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=255), Regexp(LETTERS_REGEXP)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=255), Regexp(LETTERS_REGEXP)])
    age = IntegerField('Age', validators=[InputRequired(), NumberRange(min=18, max=130)])
    tel_number = StringField('Phone number', validators=[InputRequired(), Regexp(r'^[0-9]{11}$', message=PH_NUM_MESS)])
    email = StringField('Email', validators=[InputRequired(), Length(max=100), Email()])


class RoomReservationForm(FlaskForm):
    room_number = SelectField('Room number', validators=[InputRequired()], choices=[])
    start_date = DateField('Start date', validators=[InputRequired(), NotPastValidator()])
    end_date = DateField('End date', validators=[InputRequired(), AfterStartValidator(), NotPastValidator()])
    num_of_people = IntegerField('Number of people', validators=[InputRequired(), NumberRange(min=1, max=20)])


class EquipmentReservationForm(FlaskForm):
    eq_category = SelectField('Category', validators=[InputRequired()], choices=[])
    eq_name = SelectField('Equipment', validators=[InputRequired()], choices=[])
    start_date = DateField('Start date', validators=[InputRequired(), NotPastValidator()])
    start_date_hour = TimeField('Start hour', validators=[InputRequired()])
    end_date = DateField('End date', validators=[InputRequired(), AfterStartValidator(), NotPastValidator()])
    end_date_hour = TimeField('End hour', validators=[InputRequired()])
