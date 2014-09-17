from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

class ContactsView(TemplateView):
    template_name = "contacts.tpl"

class FavoritesView(TemplateView):
    template_name = "favorites.tpl"

class EulaView(TemplateView):
    template_name = "eula.tpl"