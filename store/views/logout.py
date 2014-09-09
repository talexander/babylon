# --*-- coding: utf-8 --*--

from django.views.generic.base import RedirectView
from django.contrib.auth import logout

class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        if request.user is not None:
            if request.user.is_authenticated():
                logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
