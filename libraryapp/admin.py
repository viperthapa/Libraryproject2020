from django.contrib import admin
from .models import *

admin.site.register([Contact, Libranian, Program, Student,
                     BookCategory, Publisher, Author, Book, Issue, Return])

# Register your models here.
