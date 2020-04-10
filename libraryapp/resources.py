from import_export import resources
from .models import BookRating,Book

class BookRatingResource(resources.ModelResource):
    class Meta:
        model = BookRating


class BookResource(resources.ModelResource):
    class Meta:
        model = Book