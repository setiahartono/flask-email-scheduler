from flask_admin.contrib.sqla import ModelView

from . import db, admin


# Mixin to easily insert instance to database
class InsertMixin(object):
    def create(self):
        db.session.add(self)
        db.session.commit()


# Model definition starts here
class Contact(InsertMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_email = db.Column(db.String(120), unique=True)
    events = db.relationship('Event', backref="contact", lazy=False)

    def __repr__(self):
        return self.contact_email


class Event(InsertMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    schedules = db.relationship('EmailSchedule', backref="event", lazy=True)

    def __repr__(self):
        return "Event ID: {} - Contact: {}".format(self.id, self.contact)


class EmailSchedule(InsertMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    email_subject = db.Column(db.String(255))
    email_content = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime)

    @property
    def contact_email(self):
        return self.event.contact.contact_email

    def __repr__(self):
        return "Event ID: {} - Contact: {} - Timestamp: {}".format(self.event_id, self.event.contact, self.timestamp)


db.create_all()
# db.session.commit()


# Admin definition starts here
class ContactView(ModelView):
    form_excluded_columns = ['events']


class EventView(ModelView):
    form_excluded_columns = ['schedules']


admin.add_view(ContactView(Contact, db.session))
admin.add_view(EventView(Event, db.session))
admin.add_view(ModelView(EmailSchedule, db.session))
