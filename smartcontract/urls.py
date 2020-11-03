from django.conf.urls import url
from . import views

app_name = 'smartcontract'

urlpatterns = [
    url(r'^product/$', views.product_list, name="list"),
    url(r'^product/create/$', views.product_new, name="create"),
    url(r'^product/(?P<id>[\w-]+)/$', views.product_disp, name="disp"),
]