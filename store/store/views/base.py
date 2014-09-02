# -*- coding: utf-8 -*-

from store import  settings
from store import models
import random

class BaseView:
    def common_vars(self):
        return {
            'page': {'title': settings.SITE_NAME},
            'rand': random.randint(1, 1000000)
        }

