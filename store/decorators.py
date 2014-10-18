# --*-- coding: utf-8 --*--
from django.core.cache import cache
import logging
from django.core.cache import cache
from functools import wraps

# logger = logging.getLogger(__name__)
logger = logging.getLogger('django.request')


def cached_object(key_prefix, ttl = 30):
    def _decorator(fn):
        def wrapper(self, *args, **kwargs):
            try:
                key = '%s__%s__%d' % (key_prefix, self.__class__.__name__, self.id)
                data = cache.get(key)
                if data is not None:
                    return data
                data =  fn(self, *args, **kwargs)
                cache.set(key, data, 30)
                return data
            except Exception as e:
                logger.error(e)
            return fn(self, *args, **kwargs)
        return wrapper


    return _decorator

