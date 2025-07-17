import os
import django
from datetime import date

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from mywebsite.models import Publisher, Book, Member, Order


def load_data():
    print("Loading publishers...")
    # Create Publishers
    publishers_data = [
        {'name': 'Wiley', 'website': 'https://www.wiley.com/', 'city': 'Hoboken', 'country': 'USA'},
        {'name': 'Pearson', 'website': 'https://www.pearson.com/', 'city': 'London', 'country': 'England'},
        {'name': 'Random House', 'website': 'http://www.randomhousebooks.com/', 'city': 'New York', 'country': 'USA'}
    ]

    publishers = {}
    for pub_data in publishers_data:
        publisher, created = Publisher.objects.get_or_create(**pub_data)
        publishers[pub_data['name']] = publisher
        print(f"{'Created' if created else 'Found'} publisher: {publisher.name}")

    print("\nLoading books...")
    # Create Books
    books_data = [
        {'title': 'Advanced Optical Networks', 'category': 'S', 'num_pages': 110, 'price': 98.99, 'publisher': 'Wiley'},
        {'title': 'Wireless Networks', 'category': 'S', 'num_pages': 300, 'price': 187.54, 'publisher': 'Pearson'},
        {'title': 'A New World', 'category': 'T', 'num_pages': 75, 'price': 60.00, 'publisher': 'Random House'},
        {'title': 'Python Programming', 'category': 'S', 'num_pages': 275, 'price': 125.99, 'publisher': 'Pearson'},
        {'title': 'A Good Story', 'category': 'F', 'num_pages': 155, 'price': 15.00, 'publisher': 'Random House'},
        {'title': 'Jane Austen', 'category': 'B', 'num_pages': 360, 'price': 45.50, 'publisher': 'Random House'},
        {'title': 'Jane Eyre', 'category': 'F', 'num_pages': 280, 'price': 9.99, 'publisher': 'Random House'},
        {'title': 'Art History', 'category': 'O', 'num_pages': 430, 'price': 155.75, 'publisher': 'Wiley'}
    ]

    books = {}
    for book_data in books_data:
        publisher_name = book_data.pop('publisher')
        book_data['publisher'] = publishers[publisher_name]
        book, created = Book.objects.get_or_create(**book_data)
        books[book_data['title']] = book
        print(f"{'Created' if created else 'Found'} book: {book.title}")

    print("\nLoading members...")
    # Create Members
    members_data = [
        {'username': 'john', 'first_name': 'John', 'last_name': 'Smith', 'status': 2,
         'address': '123 University Avenue', 'city': 'Windsor', 'province': 'ON', 'last_renewal': date(2024, 2, 28),
         'auto_renew': True},
        {'username': 'mary', 'first_name': 'Mary', 'last_name': 'Hall', 'status': 1, 'address': '456 Sunset Avenue',
         'city': 'Windsor', 'province': 'ON', 'last_renewal': date(2024, 2, 14), 'auto_renew': True},
        {'username': 'alan', 'first_name': 'Alan', 'last_name': 'Jones', 'status': 1, 'address': '789 King Street',
         'city': 'Calgary', 'province': 'AB', 'last_renewal': date(2024, 3, 22), 'auto_renew': False},
        {'username': 'josh', 'first_name': 'Josh', 'last_name': 'Jones', 'status': 3, 'address': '456 Sunset Avenue',
         'city': 'Montreal', 'province': 'QC', 'last_renewal': date(2024, 2, 10), 'auto_renew': False},
        {'username': 'bill', 'first_name': 'Bill', 'last_name': 'Wang', 'status': 2, 'address': '', 'city': 'Edmonton',
         'province': 'AB', 'last_renewal': date(2024, 2, 28), 'auto_renew': True},
        {'username': 'anne', 'first_name': 'Anne', 'last_name': 'Wang', 'status': 2, 'address': '102 Curry Avenue',
         'city': 'Edmonton', 'province': 'AB', 'last_renewal': date(2024, 4, 2), 'auto_renew': True}
    ]

    members = {}
    for member_data in members_data:
        try:
            member = Member.objects.get(username=member_data['username'])
            print(f"Found existing member: {member.username}")
        except Member.DoesNotExist:
            member = Member.objects.create_user(
                username=member_data['username'],
                password='password123',  # Default password
                first_name=member_data['first_name'],
                last_name=member_data['last_name'],
                email=f"{member_data['username']}@example.com"
            )
            # Set additional fields
            member.status = member_data['status']
            member.address = member_data['address']
            member.city = member_data['city']
            member.province = member_data['province']
            member.last_renewal = member_data['last_renewal']
            member.auto_renew = member_data['auto_renew']
            member.save()
            print(f"Created member: {member.username}")

        members[member_data['username']] = member

    print("\nSetting up borrowed books...")
    # Set borrowed books for members (from the data file)
    borrowed_books_data = {
        'john': ['Advanced Optical Networks', 'Wireless Networks', 'A New World', 'Python Programming'],
        'mary': ['Advanced Optical Networks', 'A New World'],
        'bill': ['A New World', 'Jane Eyre', 'Art History']
    }

    for username, book_titles in borrowed_books_data.items():
        member = members[username]
        for book_title in book_titles:
            if book_title in books:
                member.borrowed_books.add(books[book_title])
        member.save()
        print(f"Set borrowed books for {username}")

    print("\nLoading orders...")
    # Create Orders
    orders_data = [
        {'member': 'john', 'books': ['Advanced Optical Networks', 'Wireless Networks'], 'order_type': 1,
         'order_date': date(2024, 3, 2)},
        {'member': 'john', 'books': ['A New World', 'Python Programming'], 'order_type': 1,
         'order_date': date(2024, 2, 19)},
        {'member': 'mary', 'books': ['Advanced Optical Networks', 'A New World'], 'order_type': 1,
         'order_date': date(2024, 3, 2)},
        {'member': 'alan', 'books': ['Wireless Networks'], 'order_type': 1, 'order_date': date(2024, 3, 24)},
        {'member': 'bill', 'books': ['A New World', 'Jane Eyre', 'Art History'], 'order_type': 1,
         'order_date': date(2024, 3, 2)},
        {'member': 'mary', 'books': ['A Good Story', 'Jane Austen'], 'order_type': 0, 'order_date': date(2024, 2, 25)},
        {'member': 'josh', 'books': ['A Good Story', 'Art History'], 'order_type': 0, 'order_date': date(2024, 3, 2)}
    ]

    for order_data in orders_data:
        member = members[order_data['member']]
        book_titles = order_data['books']

        order = Order.objects.create(
            member=member,
            order_type=order_data['order_type'],
            order_date=order_data['order_date']
        )

        for book_title in book_titles:
            if book_title in books:
                order.books.add(books[book_title])

        order.save()
        print(f"Created order {order.id} for {member.username}")

    print("\n✅ All data loaded successfully!")


if __name__ == "__main__":
    load_data()