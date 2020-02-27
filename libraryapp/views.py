from django.shortcuts import render
from .models import *
from django.views.generic import *
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy


# Create your views here.


class HomeView(TemplateView):
    template_name = 'libraniantemplates/libranianhome.html'


class AboutView(TemplateView):
    template_name = 'libraniantemplates/libranianabout.html'


class ServiceView(TemplateView):
    template_name = 'libraniantemplates/libranianservice.html'


class ContactView(CreateView):
    template_name = 'libraniantemplates/libraniancontact.html'
    form_class = ContactForm
    success_url = '/'


class LoginForm(FormView):
    template_name = 'libraniantemplates/login.html'
    form_class = LoginForm
    success_url = '/admin/home/'

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


class StudentListView(TemplateView):
    template_name = 'admintemplates/adminstudentlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['studentlists'] = Student.objects.all()
        return context


class StudentCreateView(CreateView):
    template_name = 'admintemplates/adminstudentcreate.html'
    form_class = StudentForm
    success_url = reverse_lazy('libraryapp:studentlist')


class StudentUpdateView(UpdateView):
    template_name = 'admintemplates/adminstudentcreate.html'
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy("libraryapp:studentlist")


class StudentDeleteView(DeleteView):
    template_name = 'admintemplates/studentdelete.html'
    model = Student
    success_url = reverse_lazy("libraryapp:studentlist")


# for borrowing books
def IssueBookView(request):
    if request.method == "POST":
        student_id = request.POST['student_id']
        student = Student.objects.get(id=student_id)
        status = "Borrowed"
        books_id = request.POST.getlist('selector')
        for book_id in books_id:
            book = Book.objects.get(id=book_id)
            b = Borrow(qty=1, status=status)
            b.save()
            b.student.add(student)
            b.book.add(book)
            return reverse_lazy('libraryapp:issue')
    students = Student.objects.all()
    books = Book.objects.all()
    datas = []
    for book in books:
        left = Issue.objects.filter(
            status="Borrowed", book__title=book.title).aggregate(Sum('qty'))
        if left['qty__sum'] is None:
            l = -1
        else:
            l = int(left['qty__sum'])
        datas.append(book.available - l)
    return render(request, "admintemplates/issuebook.html", {"datas": zip(books, datas), "students": students})

# to return book


# def returning(request):
#     if request.method == "POST":
#         b_id = int(request.POST["borrow_id"])
#         borrow = Borrow.objects.get(id=b_id)
#         borrow.date = datetime.now()
#         borrow.status = "Returned"
#         borrow.save()
#         return redirect('library:returning')
#     borrows = Borrow.objects.all()
#     return render(request, "student/return.html", {"borrows": borrows})
