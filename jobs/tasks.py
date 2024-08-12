from celery import shared_task
from datetime import datetime, timedelta
from jobs.models import Job
import pytz
import logging
logger = logging.getLogger(__name__)

class JobExecutor:
    def __init__(self, job):
        self.job = job
        self.now = datetime.now(pytz.timezone('Asia/Kolkata'))

    def should_execute(self):
        schedule_time = self.job.schedule_time.astimezone(self.now.tzinfo)
        if self.job.is_weekly:
            return self._should_execute_weekly(schedule_time)
        return self._should_execute_one_time(schedule_time)

    def _should_execute_weekly(self, schedule_time):
        return (schedule_time.weekday() == self.now.weekday() and
                schedule_time.time() <= self.now.time() and
                (self.job.last_run_timestamp is None or
                 self.job.last_run_timestamp < self.now - timedelta(days=7)))

    def _should_execute_one_time(self, schedule_time):
        return schedule_time <= self.now and self.job.last_run_timestamp is None

    def execute(self):
        logger.info(f"Executing Job: {self.job.name}")
        self._send_notification()
        self._update_job_timestamp()

    def _send_notification(self):
        # send_mail(subject=f"Job {self.job.name} Execution",
        #           message=f"Your job '{self.job.name}' has been executed successfully at {datetime.now(pytz.UTC)}",
        #           from_email=settings.EMAIL_HOST_USER,
        #           recipient_list=['example@gmail.com'],)
        logger.info("Message send")

    def _update_job_timestamp(self):
        self.job.last_run_timestamp=self.now
        self.job.next_run_timestamp = self.job.schedule_time + timedelta(weeks=1) if self.job.is_weekly else None
        self.job.save()

@shared_task()
def check_and_execute_jobs():
    jobs = Job.objects.all()
    for job in jobs:
        executor = JobExecutor(job)
        if executor.should_execute():
            executor.execute()
            logger.info(f"#########Mail sent for job {job.id} ##########")




