from import_export import resources
from import_export.admin import ExportMixin
from django.contrib import admin
from .models import Approved, Pending, Rejected, Deleted, NotEval, NotEvalAdmin
# Register your models here.


class ApprovedResource(resources.ModelResource):

    class Meta:
        model = Approved


@admin.site.register(Approved)
class ApprovedAdmin(ExportMixin, admin.ModelAdmin):
    exclude = ('id',)
    resource_class = ApprovedResource


class PendingResource(resources.ModelResource):

    class Meta:
        model = Pending


@admin.site.register(Pending)
class PendingAdmin(ExportMixin, admin.ModelAdmin):
    exclude = ('id',)
    resource_class = PendingResource


class RejectedResource(resources.ModelResource):

    class Meta:
        model = Rejected


@admin.site.register(Rejected)
class RejectedAdmin(ExportMixin, admin.ModelAdmin):
    exclude = ('id',)
    resource_class = RejectedResource


class DeletedResource(resources.ModelResource):

    class Meta:
        model = Deleted


@admin.site.register(Deleted)
class DeletedAdmin(ExportMixin, admin.ModelAdmin):
    exclude = ('id',)
    resource_class = DeletedResource
