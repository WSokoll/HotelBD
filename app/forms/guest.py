from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length, Regexp, Email

LETTERS_REGEXP = r'^[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+$'
PH_NUM_MESS = 'Number should look like YYYYXXXXXXXXX,' \
              ' where YYYY is the dialing code e.g. 0048 for Poland, and X’s are the digits of phone number'


# Guest's personal data form
class GuestPersonalForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=255), Regexp(LETTERS_REGEXP)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=255), Regexp(LETTERS_REGEXP)])
    age = StringField('Age', validators=[Length(min=1, max=3), Regexp(r'^[1-9]$|^[1-9][0-9]*$')])
    tel_number = StringField('Phone number', validators=[InputRequired(), Regexp(r'^[0-9]{13}$', message=PH_NUM_MESS)])
    email = StringField('Email', validators=[InputRequired(), Length(max=100), Email()])
