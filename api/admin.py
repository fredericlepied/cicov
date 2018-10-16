from django.contrib import admin
from django.contrib.auth.models import Group

from api import models


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    search_fields = ("name",)
    ordering = ("name",)


class TestAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


class RFEAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    search_fields = ("name",)
    ordering = ("name",)


class JobResultAdmin(admin.ModelAdmin):
    list_display = ("id", "build", "url", "get_product_name")
    search_fields = ("build", "url", "get_product_name")

    def get_product_name(self, obj):
        return obj.product.name

    get_product_name.short_description = "Name"
    get_product_name.admin_order_field = "product__name"


class RFEResultAdmin(admin.ModelAdmin):
    list_display = ("id", "result", "percent", "job_result", "get_rfe_name")
    search_fields = ("get_rfe_name",)

    def get_rfe_name(self, obj):
        return obj.rfe.name

    get_rfe_name.short_description = "Name"
    get_rfe_name.admin_order_field = "rfe__name"


class TestResultAdmin(admin.ModelAdmin):
    list_display = ("id", "result", "job_result", "get_test_name")
    search_fields = ("get_test_name",)

    def get_test_name(self, obj):
        return obj.test.name

    get_test_name.short_description = "Name"
    get_test_name.admin_order_field = "test__name"


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Test, TestAdmin)
admin.site.register(models.RFE, RFEAdmin)
admin.site.register(models.RFEResult, RFEResultAdmin)
admin.site.register(models.TestResult, TestResultAdmin)
admin.site.register(models.JobResult, JobResultAdmin)
admin.site.unregister(Group)
