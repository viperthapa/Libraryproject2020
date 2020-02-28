from django.shortcuts import render
from .models import *
from django.views.generic import *
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.db.models import Q


# Create your views here.


class HomeView(TemplateView):
    template_name = 'libraniantemplates/libranianhome.html'




class ContactView(CreateView):
    template_name = 'libraniantemplates/libraniancontact.html'
    form_class = ContactForm
    success_url = '/'



#login form
class LoginForm(FormView):
    template_name = 'libraniantemplates/login.html'
    form_class = LoginForm
    success_url = '/admin/book/list/'

    def form_valid(self, form):
        uname = form.cleaned_data['username']
        pword = form.cleaned_data['password']

        user = authenticate(username=uname, password=pword)
        self.thisuser = user
        if user is not None:
            login(self.request, user)
        else:
            return render(self.request, self.template_name, {'error': 'username  didnot exists', 'form': form})
        return super().form_valid(form)
    





#user registration
class UserRegistration(CreateView):
    template_name = 'libraniantemplates/register.html'
    form_class = UserForm
    success_url = '/login/'

    def form_valid(self, form):
        u_name = form.cleaned_data['username']
        pword = form.cleaned_data['password']
        user = User.objects.create_user(u_name, '', pword)
        form.instance.user = user
        # login(self.request, user)
        return super().form_valid(form)

class AdminHome(TemplateView):
    template_name = 'admintemplates/adminhome.html'


class BookListView(ListView):
    template_name = 'admintemplates/adminbooklist.html'
    queryset = Book.objects.all().order_by('-id')
    context_object_name = 'booklists'


class BookCreateView(CreateView):
    template_name = 'admintemplates/adminbookcreate.html'
    form_class = BookForm
    success_url = '/admin/book/list/'


class BooKUpdateView(UpdateView):
    template_name = 'admintemplates/adminbookcreate.html'
    model = Book
    form_class = BookForm
    success_url = reverse_lazy("libraryapp:booklist")


class BookdeleteView(DeleteView):
    template_name = 'admintemplates/adminbookdelete.html'
    model = Book
    success_url = reverse_lazy("libraryapp:booklist")


#search view

class SearchView(TemplateView):
    template_name = 'admintemplates/searchresult.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get("search")
        books = Book.objects.filter(
            Q(title__icontains=keyword) | Q(author__icontains=keyword))
        categorys = BookCategory.objects.filter(Q(title__icontains=keyword))
        context['books'] = books
        context['categorys'] = categorys

        return context
