from flask import render_template

from feedback.app import create_app
from feedback.utils import send_email


def run():
    app = create_app()
    with app.app_context():
        send_email(
            'Test E-mail',
            'mdcfeedbackdev@gmail.com',
            ['mdcfeedbackdev@gmail.com'],
            render_template('email/followup_notification.txt'),
            render_template('email/followup_notification.html'))

if __name__ == '__main__':
    run()
