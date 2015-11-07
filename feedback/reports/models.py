# -*- coding: utf-8 -*-
import arrow

from flask import (
    render_template, current_app,
    url_for
)

from feedback.database import (
    Column, db, Model
)
from feedback.utils import send_email


class Monthly(Model):
    ''' The monthly report model - this only contains
    one field: a string of e-mails separated by commas
    if necessary.
    '''
    __tablename__ = 'monthly-report'

    id = Column(db.Integer, primary_key=True, index=True)
    email_list = Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<Monthly(id:{0}, emails:{1})>'.format(
            self.id,
            self.email_list)

    def send_report(self):
        ''' From an instance of the Monthly model, send
        out an e-mail saying that this months monthly
        report is ready. This gets pinged from a server
        task every month through Heroku. In theory.
        '''
        if self.email_list is None:
            subj = 'Permitting Inspection Center Monthly Status Report'
            current_app.logger.info(
                'NO-EMAIL-ADDRESS | Subject: {}'.format(subj))
        else:
            subj = 'Permitting Inspection Center Monthly Status Report - {}'
            from_email = current_app.config.get('ADMIN_EMAIL')

            last_month = arrow.utcnow().replace(months=-1)
            date_start, date_end = last_month.span('month')
            date_header = date_start.format('MMMM, YYYY')
            year = last_month.format('YYYY')
            month = last_month.format('MM')
            report = url_for(
                'reports.overview', _external=True,
                year=year, month=month)

            send_email(
                subj.format(date_header),
                from_email,
                self.email_list,
                render_template('email/monthly_notification.txt',
                                date_header=date_header,
                                report=report),
                render_template('email/monthly_notification.html',
                                date_header=date_header,
                                report=report))
