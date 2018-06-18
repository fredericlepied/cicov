from django.conf.urls import url
from cicovapp import views

urlpatterns = [
    url(r'^products/$', views.product_list),
    url(r'^product/(?P<pk>[0-9]+)/$', views.product_detail),
]
