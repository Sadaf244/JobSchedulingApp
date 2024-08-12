from django.urls import path
from . import views

urlpatterns = [
    path('create-job/', views.CreateJob.as_view()),
    path('get-job-by-id/<int:job_id>/', views.GetJob.as_view()),
    path('get-job-list-by-user/', views.GetAllJob.as_view()),
    ]