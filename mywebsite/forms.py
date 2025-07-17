from django import forms
from mywebsite.models import Order, Book


class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [
        ('B', 'Borrow'),
        ('P', 'Purchase'),
    ]
    feedback = forms.ChoiceField(choices=FEEDBACK_CHOICES)


class SearchForm(forms.Form):
    # Get category choices from the Book model
    CATEGORY_CHOICES = [
        ('S', 'Science&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]

    name = forms.CharField(
        max_length=100,
        required=False,
        label='Your Name'
    )

    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + CATEGORY_CHOICES,
        required=False,
        label='Select a category:',
        widget=forms.RadioSelect
    )

    max_price = forms.IntegerField(
        min_value=0,
        label='Maximum Price',
        required=True
    )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'member', 'order_type']
        widgets = {
            'books': forms.CheckboxSelectMultiple(),
            'order_type': forms.RadioSelect
        }
        labels = {
            'member': 'Member name',
        }