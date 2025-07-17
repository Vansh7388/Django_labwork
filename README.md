# Django Lab Work

This is a Django web application project containing various features and functionalities.

## Project Structure

- **DjangoProject/**: Main Django project configuration
- **mywebsite/**: Django app containing models, views, templates, and static files
- **manage.py**: Django management script

## Features

- Models for data management
- Template-based views
- Static file serving
- Database migrations
- Admin interface

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/Vansh7388/Django_labwork.git
cd Django_labwork
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install django
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

6. Visit `http://127.0.0.1:8000/` in your browser to view the application.

## Database

The project uses SQLite as the default database. The database file (`db.sqlite3`) is excluded from version control.

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.
