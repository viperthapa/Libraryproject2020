from django.shortcuts import render
from .models import *
from django.views.generic import *
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .recommendation_engine import RecommendationiEngine

# Create your views here.


"""
------------------------------------------------------------
    GLOBAL CORRELATION VALUE
    THE HIGHER THE VALUE , MORE ACCURATE RESULTS
    LIMIT = [0-1]
------------------------------------------------------------
"""
CORRELATION_VALUE = 0.6         # set this value in range of (0, 1)


class HomeView(TemplateView):
    template_name = 'libraniantemplates/libranianhome.html'


class ContactView(CreateView):
    template_name = 'libraniantemplates/libraniancontact.html'
    form_class = ContactForm
    success_url = '/'


# login form
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


# logout
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/login/')

# user registration


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

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        recommender = RecommendationiEngine()
        recommended_book_title = recommender.get_recommendation(
            self.request.user.id, CORRELATION_VALUE)
        print('recommended_book_title = ', recommended_book_title)
        recommended_book = []

        for book in Book.objects.filter(title__in=recommended_book_title):
            recommended_book.append(book)
        recommended_book = Book.objects.filter(
            title__in=recommended_book_title)
        print('recommended_book = ', recommended_book)

        context['recommendation'] = recommended_book  # ['DAA', 'DBA']
        return context

    # def get_success_url(self):
    #     user_id = self.request.user.id # Get user_id from request


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


# search view

class SearchView(TemplateView):
    template_name = 'admintemplates/searchresult.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get("search")
        books = Book.objects.filter(
            Q(title__icontains=keyword) | Q(author__icontains=keyword))
        # categorys = BookCategory.objects.filter(Q(title__icontains=keyword))
        categorys = BookCategory.objects.all()
        print(categorys, '********************')
        recommender = RecommendationiEngine()
        # recommended_book_category = recommender.get_recommendation(self.request.user.id, 0.1)
        # print(recommended_book_category,'recommended_book_category')

        # recommended_book = Book.objects.filter(category_title=recommended_book_category)
        # print('recommended_book = ',recommended_book)
        context['books'] = books
        context['categorys'] = categorys

        similar_books_title = []
        print(similar_books_title, "~~~~")

        for book in books:
            similar_books_title.append(book.title)

        print("***********SIMILAR BOOK: ", type(similar_books_title))
        recommended_book_title = recommender.get_recommendation_from_category(
            similar_books_title, CORRELATION_VALUE)
        print('*******', recommended_book_title)

        recommended_book = Book.objects.filter(
            title__in=recommended_book_title)
        print('&&&&&&', recommended_book)

        print('recommended_book = ', recommended_book)

        context['recommendation'] = recommended_book  # ['DAA', 'DBA']

        return context

    def get_queryset(self):
        category_pk = self.request.GET.get('pk', None)
        print('category pk', category_pk)
        if category_pk:
            return Book.objects.filter(Book___pk=category_pk).order_by("id")
        return Book.objects.order_by("id")


def Bookdetail(request, pk):
    book = get_object_or_404(Book, id=pk)
    if request.method == "POST":
        rate = request.POST['rating']
        ratingObject = BookRating()
        # print(ratingObject.user.id,"********")
        # print(ratingObject.request.user,'***')
        ratingObject.user = request.user
        ratingObject.book = book
        ratingObject.rating = rate
        ratingObject.save()
        messages.success(request, "Your Rating is submited ")
        return redirect("libraryapp:booklist")
    return render(request, 'admintemplates/bookrating.html', {'book': book})

#user list 
def UserList(request):
    user = User.objects.all()
    context = {
        'user':user
    }
    return render(request,'libraniantemplates/user_list.html',context)