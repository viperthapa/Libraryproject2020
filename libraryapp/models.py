from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.
from django.core.validators import MaxValueValidator, MinValueValidator


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=120)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Libranian(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Admin')
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='admin')
        self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



SEMESTER = (
    ('semester 1', 'SEMESTER I'),
    ('semester 2', 'SEMESTER II'),
    ('semester 3', 'SEMESTER III'),
    ('semester 4', 'SEMESTER IV'),
    ('semester 5', 'SEMESTER V'),
)

SECTION = (
    ('section A', 'section A'),
    ('section B', 'section B'),
    ('section C', 'section C'),
    ('section D', 'section D'),



)


class NormalUser(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    semester = models.CharField(max_length=100, choices=SEMESTER)
    section = models.CharField(max_length=100, choices=SECTION)
    image = models.ImageField(upload_to='student')

    
    def save(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='normaluser')
        self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class BookCategory(TimeStamp):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='bookcategory')

    def __str__(self):
        return self.title


class Publisher(TimeStamp):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='publisher')
    website = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Author(TimeStamp):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='author')

    def __str__(self):
        return self.name




rating = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),




)
class Book(TimeStamp):
    title = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100)
    category = models.ForeignKey(BookCategory,on_delete=models.CASCADE)
    # publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    # author = models.ManyToManyField(Author)
    publisher= models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to = 'book')
    available = models.IntegerField(default=0)



    def __str__(self):
        return self.title




class BookRating(models.Model):
	user   	= models.ForeignKey(User,on_delete=models.CASCADE,null =True) 
	book 	= models.ForeignKey(Book,on_delete=models.CASCADE,null =True)
	rating 	= models.IntegerField(default=1,validators=[MaxValueValidator(5),MinValueValidator(0)])
		
# class BookRating(model.Model):
#     book = models.ForeignKey(Book,on_delete = models.CASCADE)
