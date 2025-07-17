# Import necessary classes
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Publisher, Book, Member, Order
from .forms import FeedbackForm, SearchForm, OrderForm

# Import necessary classes and models for authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


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


# Authentication Views
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('mywebsite:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'mywebsite/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('mywebsite:index'))


# PART 1: Feedback Form View
def getFeedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            if feedback == 'B':
                choice = ' to borrow books.'
            elif feedback == 'P':
                choice = ' to purchase books.'
            else:
                choice = ' None.'
            return render(request, 'mywebsite/fb_results.html', {'choice': choice})
        else:
            return HttpResponse('Invalid data')
    else:
        form = FeedbackForm()
        return render(request, 'mywebsite/feedback.html', {'form': form})


# PART 2 & 3: Search Form View (updated version)
def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']

            # Filter books by max_price first
            booklist = Book.objects.filter(price__lte=max_price)

            # If category is selected, filter by category too
            if category:
                booklist = booklist.filter(category=category)

            return render(request, 'mywebsite/results.html', {
                'name': name,
                'category': category,
                'booklist': booklist
            })
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'mywebsite/findbooks.html', {'form': form})


# PART 4: Place Order View
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            books = form.cleaned_data['books']
            order = form.save(commit=False)
            member = order.member
            type = order.order_type
            order.save()

            # Add the many-to-many relationships after saving
            form.save_m2m()

            if type == 1:  # Borrow
                for b in order.books.all():
                    member.borrowed_books.add(b)

            return render(request, 'mywebsite/order_response.html', {
                'books': books,
                'order': order
            })
        else:
            return render(request, 'mywebsite/placeorder.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'mywebsite/placeorder.html', {'form': form})