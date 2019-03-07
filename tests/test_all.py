import os

from datetime import datetime
from flask_testing import TestCase
from mock import patch

from scheduler_app import db
from scheduler_app.app import app
from scheduler_app.config import BASEDIR
from scheduler_app.models import Contact, Event, EmailSchedule
from scheduler_app.tasks import check_scheduled_emails


class TestAll(TestCase):
    def create_app(self):
        self.db_path = "{}/db/{}".format(BASEDIR, "email_post_test.sqlite3")
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(self.db_path)
        app.config["TESTING"] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        with app.app_context():
            self.client = app.test_client()

        db.init_app(app)
        db.create_all()
        self.contact = Contact(contact_email="bayu.setiahartono@gmail.com")
        db.session.add(self.contact)
        db.session.commit()
        self.event = Event(contact_id=self.contact.id)
        db.session.add(self.event)
        db.session.commit()
        self.email_schedule = EmailSchedule(
            event_id=self.event.id,
            email_subject="Sample Subject",
            email_content="Sample Content",
            timestamp=datetime(2019, 1, 1, 0, 0, 0)
        )
        db.session.add(self.email_schedule)
        db.session.commit()

    def tearDown(self):
        os.remove(self.db_path)

    # Test model section
    def test_contact_repr(self):
        self.assertEqual(self.contact.__repr__(), self.contact.contact_email)

    def test_event_repr(self):
        expected_repr = "Event ID: {} - Contact: {}".format(self.event.id, self.event.contact)
        self.assertEqual(self.event.__repr__(), expected_repr)

    def test_email_schedule_repr(self):
        expected_repr = "Event ID: {} - Contact: {} - Timestamp: {}".format(
            self.email_schedule.event_id,
            self.email_schedule.contact_email,
            self.email_schedule.timestamp
        )
        self.assertEqual(self.email_schedule.__repr__(), expected_repr)

    # Test client section
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_save_emails(self):
        self.assertEqual(len(EmailSchedule.query.all()), 1)
        valid_data = {
            "event_id": self.event.id,
            "email_subject": "Test Subject",
            "email_content": "Sample body content",
            "timestamp": "01 Jan 2019 00:00",
        }
        response = self.client.post("/save_emails", data=valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(EmailSchedule.query.all()), 2)

        invalid_data = {
            # existing event id plus one to ensure invalid event id
            "event_id": self.event.id + 1,
            "email_subject": "Test Subject",
            "email_content": "Sample body content",
            "timestamp": "01 Jan 2019 00:00",
        }
        invalid_response = self.client.post("/save_emails", data=invalid_data)
        self.assertEqual(invalid_response.status_code, 302)
        self.assertEqual(len(EmailSchedule.query.all()), 2)

    # Test celery task section
    def test_check_scheduled_email(self):
        with patch('scheduler_app.tasks.send_email.delay'):
            email_schedule_now = EmailSchedule(
                event_id=self.event.id,
                email_subject="Sample Subject",
                email_content="Sample Content",
                timestamp=datetime.now()
            )
            db.session.add(email_schedule_now)
            db.session.commit()
            check_scheduled_emails()
