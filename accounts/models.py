from django.contrib.auth.models import AbstractUser
from django.db import models
import re
import logging


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return self.username


class UserSignupValidation:

    def validate_signup_data(self, username, email):
        errors = {}
        if not username or username.strip() == "":
            errors = 'Username is required'
        elif not email or email.strip() == "":
            errors = 'Email address is required'
        elif CustomUser.objects.filter(username=username).exists():
            errors = 'Username is already in use'
        elif CustomUser.objects.filter(email=email).exists():
            errors = 'Email address is already in use'

        email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

        if not email_regex.match(email):
            errors = 'Please provide a valid email address (e.g., username@gmail.com)'

        if errors:
            return {'resp_dict': {'status': False, 'message': errors}}
        return {'resp_dict': {'status': True, 'message': 'Validation successful'}}


class UserAccountManager:
    def __init__(self, request):
        self.request = request

    def start_on_boarding(self):
        username = self.request.data.get('username')
        email = self.request.data.get('email')
        password = self.request.data.get('password')
        validator = UserSignupValidation()
        validation_result = validator.validate_signup_data(username, email)
        resp_dict = validation_result['resp_dict']
        if not resp_dict['status']:
            return resp_dict

        try:

            CustomUser.objects.create_user(username=username, email=email, password=password)
            resp_dict.update({
                'status': True,
                'message': 'User account created successfully'
            })
        except Exception as e:
            logging('getting exception on start_on_boarding', repr(e))
        return resp_dict