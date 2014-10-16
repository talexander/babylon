# -*- coding: utf-8 -*-
from store import models

def intval(val):
    try:
        return int(val)
    except Exception, e:
        return 0

def get_cart_items(str):
    items = []
    if(len(str) > 0 ):
        data = str.split(';')

        for pair in data:
            try:
                r = {}
                v = pair.split(':')
                r['id'] = v[0]
                r['count'] = v[-1]
                v2 = r['id'].split('_')
                if len(v2) > 1:
                    r['id'] = v2[0]
                    r['sku'] = v2[-1]
                r['product'] = models.Good.objects.get(pk=r['id'])
                if r.get('sku', False):
                    r['sku'] = r['product'].sku(r.get('sku'))
                r['summ'] = r['product'].price * intval(r['count'])

                items.append(r)
            except Exception,e:
                continue
    return items

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

