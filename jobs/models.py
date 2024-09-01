from django.db import models
from accounts.models import CustomUser
import logging


class Job(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_weekly = models.BooleanField(default=False)
    after_days = models.IntegerField(null=True, blank=True,default=0)
    schedule_time = models.DateTimeField()
    last_run_timestamp = models.DateTimeField(null=True, blank=True)
    next_run_timestamp = models.DateTimeField(null=True, blank=True)
    job_parameters = models.JSONField(default=dict)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]

    @staticmethod
    def create_job(user, name, is_weekly, schedule_time, after_days):

        obj = Job.objects.create(user=user, name=name,is_weekly=is_weekly,schedule_time=schedule_time, after_days= after_days)
        return obj

    @staticmethod
    def get_job_object_on_id(job_id=None):
        job_object = None
        if job_id:
            try:
                job_object = Job.objects.get(id=job_id)
                print(job_object)
            except Exception as e:
                logging.error('getting exception on get_job_object_on_id', repr(e))
        return job_object

    @staticmethod
    def get_job_on_user(user=None):
        job = None
        if user:
            try:
                job = Job.objects.filter(user=user).values(
                    'name',
                    'schedule_time',
                    'last_run_timestamp',
                    'next_run_timestamp'
                )
            except Exception as e:
                logging.error('getting exception on get_job_on_user', repr(e))
        return job


class CreateJobManager:
    def __init__(self, user, requested_data):
        self.user = user
        self.requested_data = requested_data

    def save_user_job(self):
        resp_dict = dict(status=False, message="Something went wrong")
        try:
            name = self.requested_data.data.get('name', None)
            is_weekly = self.requested_data.data.get('is_weekly', None)
            schedule_time = self.requested_data.data.get('schedule_time', None)
            after_days = self.requested_data.data.get('after_days', 0)

            if name is not None and is_weekly is not None and schedule_time is not None:
                Job.create_job(self.user, name, is_weekly, schedule_time, after_days)
                resp_dict['status'] = True
                resp_dict['message'] = "Job Created and Scheduled Successfully"
        except Exception as e:
            logging.error('getting exception on save_user_job', repr(e))
        return resp_dict


class GetJobManager:

    def __init__(self, job_id):
        self.job_id=job_id
        self.job_obj = Job.get_job_object_on_id(self.job_id)
        self.job_dict = self.job_obj.__dict__ if self.job_obj else dict()

    def get_user_job(self):
        resp_dict = dict(status=False, message="Something went wrong", data=dict())
        try:

            if self.job_obj is not None:
                job_detail = {
                    "job_name": self.job_dict['name'],
                    "schedule_time": self.job_dict['schedule_time'],
                    "last_run_timestamp": self.job_dict['last_run_timestamp'],
                    "next_run_timestamp": self.job_dict['next_run_timestamp'],
                }
                resp_dict['data'] = job_detail
                resp_dict['status'] = True
                resp_dict['message'] = "Got Job Successfully"
        except Exception as e:
            logging.error('getting exception on get_user_job', repr(e))
        return resp_dict


class GetAllJobManager:
    def __init__(self, user):
        self.user = user
        self.job = Job.get_job_on_user(self.user)


    def get_user_job_list(self):
        resp_dict = dict(status=False, message="Something went wrong", data=dict())
        try:
            if self.job:

                data_list = []
                for job in self.job:
                    job_data = {
                        "job_name": job['name'],
                        "schedule_time": job['schedule_time'],
                        "last_run_timestamp": job['last_run_timestamp'],
                        "next_run_timestamp": job['next_run_timestamp'],
                    }
                    data_list.append(job_data)

                resp_dict['data'] = data_list
                resp_dict['status'] = True
                resp_dict['message'] = "Got Job Successfully"
        except Exception as e:
            logging.error('getting exception on get_user_job_list', repr(e))
        return resp_dict



