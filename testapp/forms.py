from flask_wtf import FlaskForm
from wtforms import SubmitField


class Cookie(FlaskForm):
    submit = SubmitField('Give me a cookie')
