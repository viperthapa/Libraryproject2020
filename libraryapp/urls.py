from django.conf.urls import url
from .views import *
from django.urls import path
from . import views

app_name = 'libraryapp'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('login/', LoginForm.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('user/registration/', UserRegistration.as_view(),
         name='userregistration'),
    path('admin/home/', AdminHome.as_view(), name='adminhome'),
    path('admin/book/list/', BookListView.as_view(), name='booklist'),
    path('admin/book/create/', BookCreateView.as_view(), name='bookcreate'),
    path('admin/book/update/<int:pk>/',
         BooKUpdateView.as_view(), name='bookupdate'),
    path('admin/book/delete/<int:pk>/',
         BookdeleteView.as_view(), name='bookdelete'),
    path("search/", SearchView.as_view(), name='search'),
    path('book/<int:pk>/',views.Bookdetail ,name='bookdetail'),
    path('user/list/',views.UserList,name = "userlist"),
    


   



]
