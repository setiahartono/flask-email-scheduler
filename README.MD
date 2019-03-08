# Flask Email Scheduler

## Description
A mini project on implementing task scheduler using Flask, Celery and Redis (can be changed to RabbitMQ).
Repository includes the app, admin page, config, and automated test.

## How it works
Every minute Celery Beat will check for stored schedule by using ORM filter. If a scheduled instance at current time found, the scheduler will push the email sending task into queue.

## Development stack
* Python 3.4
* Virtualenv
* Flask-Admin
* Flask Micro Framework
* Flask-SQLALchemy for the ORM
* Flask-Testing for testing purpose
* Celery for queueing task
* Celery Beat for scheduling

## Installation
* Clone the repository
* Create a virtual environment `virtualenv -p python3 env_name`
* Run `source /path/to/env_name`
* Go to project main directory and run `pip install -r requirements.txt`
* Check `scheduler_app/config.py`, modify as needed

## Running Automated Test
* Make sure that you're running an virtual environment (`source /path/to/env_name`)
* Run test `coverage run --source scheduler_app -m pytest --disable-pytest-warnings`
* Write the code coverage into html `coverage html`
* Or just go into project directory, run `. run_tests.sh` to build tests instantly
* Check code coverage in folder 'htmlcov/index.html' inside the project directory

## Running Development Server
* Make sure that you're running an virtual environment (`source /path/to/env_name`)
* Go into project main directory, run `. run_development.sh`
