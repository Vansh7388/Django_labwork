# Import necessary classes
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Publisher, Book, Member, Order


# Create your views here.
def index(request):
    response = HttpResponse()

    # Get books ordered by primary key
    booklist = Book.objects.all().order_by('id')[:10]
    heading1 = '<h2>' + 'List of available books: ' + '</h2>'
    response.write(heading1)

    for book in booklist:
        para = '<p>' + str(book.id) + ': ' + str(book) + '</p>'
        response.write(para)

    # Get publishers ordered by city in descending order
    publishers = Publisher.objects.all().order_by('-city')
    heading2 = '<h2>' + 'List of Publishers: ' + '</h2>'
    response.write(heading2)

    for publisher in publishers:
        para = '<p>' + str(publisher.name) + ' - ' + str(publisher.city) + '</p>'
        response.write(para)

    return response


def about(request):
    response = HttpResponse()
    response.write('<h1>This is an eBook APP</h1>')
    return response


def detail(request, book_id):
    # Use get_object_or_404 to handle non-existent books
    book = get_object_or_404(Book, pk=book_id)

    response = HttpResponse()
    response.write('<h1>' + book.title.upper() + '</h1>')
    response.write('<p>Price: $' + str(book.price) + '</p>')
    response.write('<p>Publisher: ' + str(book.publisher) + '</p>')

    return response