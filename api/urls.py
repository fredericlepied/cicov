from django.conf.urls import url
from rest_framework_extensions.routers import ExtendedDefaultRouter

from api import views

router = ExtendedDefaultRouter(trailing_slash=False)
router.register("products", views.ProductViewSet, base_name="product")
router.register("rfes", views.RFEViewSet, base_name="rfe")
router.register("tests", views.TestViewSet, base_name="test_id")
router.register("job_results", views.JobResultViewSet, base_name="job_result")
router.register("upload", views.FileUploadView, base_name="file_upload")

urlpatterns = [
    url(r'^view/products$', views.view_products),
    url(r'^view/get_rfes/(?P<product>[a-zA-Z0-9]+)$', views.get_rfes),
]

urlpatterns += router.urls
