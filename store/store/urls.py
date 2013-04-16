from django.conf.urls import patterns, include, url
from store.views.index import IndexView 
from store.views.login import LoginView
from store.views.register import RegisterView
from store.views.register_success import RegisterSuccessView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', IndexView.as_view()),
    url(r'^login/?$', LoginView.as_view()),
    url(r'^register/?$', RegisterView.as_view()),
    url(r'^register/success/?$', RegisterSuccessView.as_view()),

    # url(r'^store/', include('store.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

