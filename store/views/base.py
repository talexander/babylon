# -*- coding: utf-8 -*-

from store import  settings
from store import models
import random

class BaseView:
    def common_vars(self):
        return {
            'page': {
                'title': self.title(),
                'seo': self.seo(),
            },
            'rand': random.randint(1, 1000000),
            'STATIC_URL': settings.STATIC_URL,
        }

    def title(self):
        return settings.SITE_NAME

    def seo(self):
        return {
            'keywords': 'нитки пряжа для ручного вязания шерсть меринос альпака полушерсть хлопок лен спицы крючки вилка для вязания интернет-магазин пряжи в Орле товары для рукоделия',
            'description': u'Интернет-магазин пряжи в Орле. Купить пряжу и аксессуары для вязания по низким ценам.',
        }


