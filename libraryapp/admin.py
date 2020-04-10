from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from import_export import resources


class BookRatingResource(resources.ModelResource):
    class Meta:
        model = BookRating
# Register your models here.
@admin.register(BookRating)
class BookRatingAdmin(ImportExportModelAdmin):
    resource_class = BookRatingResource


@admin.register(NormalUser)
class NormalUserAdmin(ImportExportModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    pass


@admin.register(BookCategory)
class BookCategoryAdmin(ImportExportModelAdmin):
    pass


admin.site.register([Contact])
