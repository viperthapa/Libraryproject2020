from django.conf.urls import url
from .views import *
from django.urls import path
from . import views

app_name = 'libraryapp'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('services/', ServiceView.as_view(), name='service'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('login/', LoginForm.as_view(), name='login'),
    path('admin/home/', AdminHome.as_view(), name='adminhome'),
    path('admin/book/list/', BookListView.as_view(), name='booklist'),
    path('admin/book/create/', BookCreateView.as_view(), name='bookcreate'),
    path('admin/book/update/<int:pk>/',
         BooKUpdateView.as_view(), name='bookupdate'),
    path('admin/book/delete/<int:pk>/',
         BookdeleteView.as_view(), name='bookdelete'),
    path('admin/student/list', StudentListView.as_view(), name='studentlist'),
    path('admin/student/create', StudentCreateView.as_view(), name='studentcreate'),
    path('admin/student/update<int:pk>', StudentUpdateView.as_view(), name='studentupdate'),
    path('admin/student/delete/<int:pk>/',
         StudentDeleteView.as_view(), name='studentdelete'),
    path('admin/student/issue/',views.IssueBookView,name = 'issue'),





]
