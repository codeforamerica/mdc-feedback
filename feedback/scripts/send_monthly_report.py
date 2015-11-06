"""
This script should run monthly to:
"""
from feedback.app import create_app
from feedback.reports.models import Monthly


def run_report():
    monthly = Monthly.query.first()
    monthly.send_report()


def run():
    app = create_app()
    with app.app_context():
        run_report()

if __name__ == '__main__':
    run()
