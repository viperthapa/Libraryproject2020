from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from import_export import resources

# Register your models here.
# @admin.register(BookRating)
# class BookRatingAdmin(ImportExportModelAdmin):
    

    
# @admin.register(Book)
# class BookAdmin(ImportExportModelAdmin):
#     pass

    


class BookRatingResource(resources.ModelResource):

    class Meta:
        model = BookRating



@admin.register(BookRating)
class BookAdmin(ImportExportModelAdmin):
    resource_class = BookRatingResource


admin.site.register([Contact,
                     BookCategory, Author,NormalUser])
