from django.conf import settings
from django.conf.urls import patterns, include, url
from store.views.index import IndexView 
from store.views.login import LoginView
from store.views.register import RegisterView
from store.views.register_success import RegisterSuccessView
from store.views.logout import LogoutView
from store.views.goods_filter import GoodsFilterView
from store.views.cart import CartView
from store.views.simple import ContactsView, FavoritesView
from store.views.order import OrderView
# from store.views.chained_select import ChainedSelectChoices
from store.views.simple import EulaView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', IndexView.as_view()),
    url(r'^filter/?$', GoodsFilterView.as_view()),
    url(r'^contacts/?$', ContactsView.as_view()),
    url(r'^favorites/?$', FavoritesView.as_view()),
    url(r'^cart/?$', CartView.as_view()),
    url(r'^product/([a-z,A-Z,0-9,\-,\+]+)/([a-z,A-Z,0-9,\-]+)/?$', IndexView.as_view(), name = 'product_url'), # @TODO: substitute correct dispatcher
    url(r'^product/(?P<category>[a-z,A-Z,0-9,\-,\+]+)/?$', GoodsFilterView.as_view(), name = 'product_category_url'), # @TODO: substitute correct dispatcher
    url(r'^order/new/?$', OrderView.as_view()),
    url(r'^order/success/?$', OrderView.as_view(**{'success': 1, 'template_name': 'order_success.tpl' })),
    url(r'^eula/?$', EulaView.as_view()),


    url(r'^login/?$', LoginView.as_view()),
    url(r'^logout/?$', LogoutView.as_view()),
    url(r'^register/?$', RegisterView.as_view()),
    url(r'^register/success/?$', RegisterSuccessView.as_view()),

    # url(r'^chainedselectchoices$', ChainedSelectChoices.as_view(), name = 'chained_select_choices'),

    # url(r'^store/', include('store.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )