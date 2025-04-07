# Quora Clone

A production-ready Django web application inspired by Quora, built with modern best practices in web development.

## Features

- User authentication (register, login, logout)
- Question posting, editing, and deletion
- Answer posting, editing, and deletion
- Liking system for answers
- User profiles
- Responsive design with Bootstrap 5

## Technology Stack

- Django 5.0.5
- SQLite (default database)
- Bootstrap 5 (frontend framework)
- Crispy Forms with Bootstrap 5 template pack

## Project Structure

The project follows a modular design with separate Django apps:

- `accounts`: Handles user authentication and profiles
- `core`: Contains base templates and shared functionality
- `questions`: Manages questions, answers, and likes

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/sanskarpan/quora-clone
cd quora_clone
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Create a superuser (admin):

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

7. Access the application at http://127.0.0.1:8000/

## Testing

Run the test suite with:

```bash
python manage.py test
```

Or run tests for a specific app:

```bash
python manage.py test accounts
python manage.py test questions
python manage.py test core
```

## Security Features

- CSRF protection
- Password hashing and validation
- User authentication required for sensitive operations
- Permission checks for editing/deleting content


## License

[MIT License](LICENSE)