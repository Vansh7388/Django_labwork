# Import necessary classes
from django.shortcuts import render, get_object_or_404
from .models import Publisher, Book, Member, Order


# Create your views here.
def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'mywebsite/index.html', {'booklist': booklist})


def about(request):
    # No extra context variables needed for basic about page
    return render(request, 'mywebsite/about.html')


def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    # Passing book object as context variable
    return render(request, 'mywebsite/detail.html', {'book': book})