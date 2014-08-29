# -*- coding: utf-8 -*-

from store import  settings
from store import models

class BaseView:
    def common_vars(self):
        return {
            'page': {'title': settings.SITE_NAME}
        }

