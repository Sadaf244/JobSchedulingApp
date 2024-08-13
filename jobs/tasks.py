from celery import shared_task
from datetime import datetime, timedelta
from jobs.models import Job
import pytz
import logging
logger = logging.getLogger(__name__)
from django.conf import settings
from django.core.mail import send_mass_mail


class JobExecutor:
    def __init__(self, jobs, now):
        self.jobs = jobs
        self.now = now
        self.notifications = []

    def process_jobs(self):
        for job in self.jobs:
            if self.should_execute(job):
                self.execute(job)

    def should_execute(self, job):
        schedule_time = job.schedule_time.astimezone(self.now.tzinfo)
        if job.is_weekly:
            return self._should_execute_weekly(job, schedule_time)
        return self._should_execute_one_time(job, schedule_time)

    def _should_execute_weekly(self, job, schedule_time):
        return (schedule_time.weekday() == self.now.weekday() and
                schedule_time.time() <= self.now.time() and
                (job.last_run_timestamp is None or
                 job.last_run_timestamp < self.now - timedelta(days=7)))

    def _should_execute_one_time(self, job, schedule_time):
        return schedule_time <= self.now and job.last_run_timestamp is None

    def execute(self, job):
        logger.info(f"Executing Job: {job.name}")
        self._prepare_notification(job)
        self._update_job_timestamp(job)

    def _prepare_notification(self, job):
        message = (
            f"Job {job.name} Execution",
            f"Hello {job.user.username} , Your job '{job.name}' has been executed successfully at {self.now}",
            settings.EMAIL_HOST_USER,
            [job.user.email],
        )
        self.notifications.append(message)

    def _update_job_timestamp(self, job):
        job.last_run_timestamp = self.now
        job.next_run_timestamp = job.schedule_time + timedelta(weeks=1) if job.is_weekly else None


@shared_task()
def check_and_execute_jobs():
    kolkata_tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(kolkata_tz)
    jobs = Job.objects.all()
    executor = JobExecutor(jobs, now)
    executor.process_jobs()
    if executor.notifications:
        send_mass_mail(tuple(executor.notifications), fail_silently=False)
        logger.info(f"############{len(executor.notifications)} Mails sent##########")
    Job.objects.bulk_update(jobs, ['last_run_timestamp', 'next_run_timestamp'])



