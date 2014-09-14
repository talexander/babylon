# -*- coding: utf-8 -*-
from store import models

def intval(val):
    try:
        return int(val)
    except Exception, e:
        return 0

def get_cart_items(str):
    if(len(str) > 0 ):
        data = str.split(';')
        items = []
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
