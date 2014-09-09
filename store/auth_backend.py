# --*-- coding: utf-8 --*--

from django.contrib.auth.models import User, make_password
from django.contrib.auth import get_user_model


class CustomBackend(object):
    def authenticate(self, email = None, password = None, **kwargs):
        UserModel = get_user_model()
        print email, password
        if email is None:
            return None
        try:
            user = UserModel._default_manager.get(email = email)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            UserModel = get_user_model()
            return UserModel._default_manager.get(pk = user_id)
        except User.DoesNotExist:
            return None

