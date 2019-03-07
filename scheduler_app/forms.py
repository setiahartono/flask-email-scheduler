from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField
from wtforms.fields import IntegerField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import InputRequired

from .models import Event


class EventForm(FlaskForm):
    event_id = IntegerField('Event ID', [InputRequired()])
    email_subject = TextField('Email Subject', [InputRequired()])
    email_content = TextAreaField('Email Content', [InputRequired()])
    timestamp = DateTimeField('Timestamp', [InputRequired()], format="%d %b %Y %H:%M")

    def validate(self):
        validate_result = super(EventForm, self).validate()
        if validate_result:
            if not Event.query.filter(Event.id == self.data['event_id']).count():
                validate_result = False
                self.errors['event_id'] = ["Invalid Event ID"]
        return validate_result
