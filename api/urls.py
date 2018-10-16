from rest_framework_extensions.routers import ExtendedDefaultRouter

from api import views

router = ExtendedDefaultRouter(trailing_slash=False)
router.register("products", views.ProductViewSet, base_name="product")
router.register("rfes", views.RFEViewSet, base_name="rfe")
router.register("tests", views.TestViewSet, base_name="test_id")
router.register("upload", views.FileUploadView, base_name="file_upload")

urlpatterns = router.urls