from import_export import resources
from .models import BookRating

class BookRatingResource(resources.ModelResource):
    class Meta:
        model = BookRating