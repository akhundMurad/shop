import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from django_celery_beat.models import IntervalSchedule, \
    CrontabSchedule, PeriodicTask


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Setup celery beat periodic tasks'

    @transaction.atomic
    def handle(self, *args, **options):
        logger.debug('Deleting all periodic tasks and schedules...')

        IntervalSchedule.objects.all().delete()
        CrontabSchedule.objects.all().delete()
        PeriodicTask.objects.all().delete()

        periodic_tasks_data = []

        for period_task in periodic_tasks_data:
            logger.debug(f'Setting up {period_task["task"].name}')

            cron = CrontabSchedule.objects.create(
                **period_task['cron']
            )

            PeriodicTask.objects.create(
                name=period_task['name'],
                task=period_task['task'].name,
                crontab=cron,
                enabled=period_task['enabled']
            )
