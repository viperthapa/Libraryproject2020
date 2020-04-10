from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

# Register your models here.
@admin.register(BookRating)
class BookRatingAdmin(ImportExportModelAdmin):
    pass

    


admin.site.register([Contact,
                     BookCategory, Author, Book,NormalUser])
