from rest_framework.views import APIView
from django.http import JsonResponse
import logging
from accounts.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from jobs.models import CreateJobManager,GetJobManager, GetAllJobManager


class CreateJob(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            user = request.user
            create_job_manager = CreateJobManager(user, request)
            save_job_resp = create_job_manager.save_user_job()
            resp_dict['status'] = save_job_resp['status']
            resp_dict['message'] = save_job_resp['message']
        except Exception as e:
            logging.error('getting exception on CreateJob', repr(e))
        return JsonResponse(resp_dict, status=200)


class GetJob(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, job_id):
        print("job_id", job_id)
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            get_job_manager = GetJobManager(job_id)
            get_job_manager_resp = get_job_manager.get_user_job()
            resp_dict['data'] = get_job_manager_resp['data']
            resp_dict['status'] = get_job_manager_resp['status']
            resp_dict['message'] = get_job_manager_resp['message']
        except Exception as e:
            logging.error('getting exception on GetJob', repr(e))
        return JsonResponse(resp_dict, status=200)


class GetAllJob(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        resp_dict = dict()
        resp_dict['status'] = False
        resp_dict['message'] = "Something went wrong. Please try again after sometime"
        try:
            get_all_job_manager = GetAllJobManager(request.user)
            get_job_manager_resp = get_all_job_manager.get_user_job_list()
            resp_dict['data'] = get_job_manager_resp['data']
            resp_dict['status'] = get_job_manager_resp['status']
            resp_dict['message'] = get_job_manager_resp['message']
        except Exception as e:
            logging.error('getting exception on GetAllJob', repr(e))
        return JsonResponse(resp_dict, status=200)