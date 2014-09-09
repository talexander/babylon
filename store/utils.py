# -*- coding: utf-8 -*-

def intval(val):
    try:
        return int(val)
    except Exception, e:
        return 0
