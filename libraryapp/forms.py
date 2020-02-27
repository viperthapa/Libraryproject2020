from django import forms
from .models import *


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'size': '70'}),)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'size': '70'}))


class BookForm(forms.ModelForm):
    # category = forms.CharField(widget=forms.TextInput())
    # publisher = forms.CharField(widget=forms.TextInput())
    # author = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Book
        fields = ['publisher','category', 'author' ,'title' , 'barcode','image']
        # fields = '__all__'


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name','program','semester','section','image']
        