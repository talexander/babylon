from django.conf import settings
from django.conf.urls import patterns, include, url
from store.views import *
from store.views.login import LoginView
from store.views.register import RegisterView
from store.views.register_success import RegisterSuccessView
from store.views.logout import LogoutView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', index.IndexView.as_view()),
    url(r'^filter/?$', goods_filter.GoodsFilterView.as_view()),
    url(r'^contacts/?$', simple.ContactsView.as_view()),
    url(r'^favorites/?$', favorites.FavoritesView.as_view()),
    url(r'^cart/?$', cart.CartView.as_view()),
    url(r'^product/(?P<category>[a-z,A-Z,0-9,\-,\+]+)/(?P<slug>[a-z,A-Z,0-9,\-]+)/?$', product.ProductView.as_view(), name = 'product_url'),
    url(r'^product/(?P<category>[a-z,A-Z,0-9,\-,\+]+)/(?P<vendor>[a-z,A-Z,0-9,\-,\+]+)/(?P<slug>[a-z,A-Z,0-9,\-]+)/?$', product.ProductView.as_view(), name = 'product_url_long'),
    url(r'^product/(?P<category>[a-z,A-Z,0-9,\-,\+]+)/?$', goods_filter.GoodsFilterView.as_view(), name = 'product_category_url'), # @TODO: substitute correct dispatcher
    url(r'^order/new/?$', order.OrderView.as_view()),
    url(r'^p/(?P<pk>\d+)/?$', product.ProductView.as_view(**{'template_name': 'api_product.tpl', 'api_call': True }), name = 'product_api_url'),
    url(r'^order/success/?$', order.OrderView.as_view(**{'success': 1, 'template_name': 'order_success.tpl' })),
    url(r'^eula/?$', simple.EulaView.as_view()),


    url(r'^login/?$', LoginView.as_view()),
    url(r'^logout/?$', LogoutView.as_view()),
    url(r'^register/?$', RegisterView.as_view()),
    url(r'^register/success/?$', RegisterSuccessView.as_view()),


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