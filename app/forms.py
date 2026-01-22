from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp

class CityForm(FlaskForm):
    city = StringField(
        "Město",
        validators=[
            DataRequired(message="Zadej město"),
            Regexp(
                "^[A-Za-zá-žÁ-Ž ]+$",
                message="Pouze písmena (safe characters)"
            )
        ]
    )
    submit = SubmitField("Zjistit počasí")
