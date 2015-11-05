"""
This script should run monthly to:
"""
from flask import (
    url_for,
    render_template, current_app
)

from feedback.app import create_app
from feedback.utils import send_email
from feedback.surveys.models import Monthly


def send_report():
    subj = 'Miami-Dade County Permit Inspection Center Monthly Report'
    from_email = current_app.config.get('ADMIN_EMAIL')
    monthly = Monthly.query.first()

    if monthly is None or monthly.email_list is None:
        current_app.logger.info(
            'NO-EMAIL-ADDRESS | Subject: {}'.format(subj))
    else:
        send_email(
            subj,
            from_email,
            monthly.email_list,
            render_template('email/monthly_notification.txt'),
            render_template('email/monthly_notification.html'))


def run():
    app = create_app()
    with app.app_context():
        send_report()

if __name__ == '__main__':
    run()
