from django.conf.urls import patterns, include, url
from store.views.index import IndexView 
from store.views.login import LoginView
from store.views.register import RegisterView
from store.views.register_success import RegisterSuccessView
from store.views.logout import LogoutView
from .views.goods_list import GoodsListView
from .views.goods_detail import GoodsDetailView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', IndexView.as_view()),
    url(r'^login/?$', LoginView.as_view()),
    url(r'^logout/?$', LogoutView.as_view()),
    url(r'^register/?$', RegisterView.as_view()),
    url(r'^register/success/?$', RegisterSuccessView.as_view()),

    url(r'^goods/?$', GoodsListView.as_view(),  name='url_goods_list'),
    url(r'^good/(?P<id>\d+)/?$', GoodsDetailView.as_view(),  name='url_goods'),

    # url(r'^store/', include('store.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

