from django.contrib import admin
from .models import *

admin.site.register([Contact,
                     BookCategory, Author, Book,NormalUser ])

# Register your models here.
