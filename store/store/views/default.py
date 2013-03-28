# -*- coding: utf-8 -*-

from django.views.generic import TemplateView

class DefaultView(TemplateView):
    template_name = "root.tpl"
