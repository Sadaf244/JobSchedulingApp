from django.contrib import admin
from .models import *
# Register your models here.
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','name', 'is_weekly', 'after_days', 'schedule_time', 'last_run_timestamp', 'next_run_timestamp')

admin.site.register(Job, JobAdmin)