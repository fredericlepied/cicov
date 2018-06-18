from django.conf.urls import url
from cicovapp import views

urlpatterns = [
    url(r'^products/$', views.product_list),
    url(r'^product/(?P<pk>[0-9]+)/$', views.product_detail),
    url(r'^rfes/$', views.rfe_list),
    url(r'^rfe/(?P<pk>[0-9]+)/$', views.rfe_detail),
    url(r'^test_ids/$', views.test_id_list),
    url(r'^test_id/(?P<pk>[0-9]+)/$', views.test_id_detail),
    url(r'^job_results/$', views.job_result_list),
    url(r'^job_result/(?P<pk>[0-9]+)/$', views.job_result_detail),
    url(r'^test_results/$', views.test_result_list),
    url(r'^test_result/(?P<pk>[0-9]+)/$', views.test_result_detail),
]
