"""
This script should run daily to:
"""
from feedback.app import create_app


def load_data():
    raise NotImplementedError


def run():
    app = create_app()
    with app.app_context():
        load_data()

if __name__ == '__main__':
    run()
