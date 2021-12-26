import logging

from tasks.apps import app


logger = logging.getLogger(__name__)


@app.task
def create_reports_for_today():
    from reporting.services import report

    logger.info('Creating reports for today...')
    report.create_reports()
