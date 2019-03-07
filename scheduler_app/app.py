from flask import request, redirect, render_template, url_for, flash

from . import app
from .forms import EventForm
from .models import EmailSchedule


@app.route('/', methods=['GET'])
def index():
    form = EventForm()
    return render_template('index.html', form=form)


@app.route('/save_emails', methods=['POST'])
def save_emails():
    form = EventForm(request.form)
    if form.validate():
        data = form.data
        email_schedule = EmailSchedule(
            event_id=data['event_id'],
            email_subject=data['email_subject'],
            email_content=data['email_content'],
            timestamp=data['timestamp'],
        )
        email_schedule.create()
        flash('Data Saved')
    else:
        for error_field in form.errors:
            errors = ", ".join(form.errors[error_field])
            error_msg = "{}: {}".format(error_field, errors)
            flash(error_msg)
    return redirect(url_for('index'))
