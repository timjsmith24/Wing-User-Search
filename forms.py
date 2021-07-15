from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired


class UserSearchForm(FlaskForm):
    site = StringField('Enter Site', validators=[DataRequired()])
    #site = SelectField("Choose Site", choices=sitelist, validators=[DataRequired()])
    user = StringField('Enter User name', validators=[DataRequired()])
    submit = SubmitField('Search')