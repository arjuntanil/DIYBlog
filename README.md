# DIYBlog - A Django Blog Platform

A full-featured blog platform built with Django, focusing on DIY (Do It Yourself) content sharing.

## Features

- User Authentication (Register, Login, Logout)
- Blog Post Management
- Password Protected Posts
- Interactive Polls
- Comments System
- Responsive Design
- Azure Deployment Ready

## Prerequisites

- Python 3.8+
- Django 4.2+
- Other dependencies listed in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd DIYBlog
```

2. Create and activate a virtual environment:
```bash
python -m venv diyblogWindSurf
source diyblogWindSurf/bin/activate  # On Windows: .\diyblogWindSurf\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser.

## Project Structure

- `blog/` - Main application directory
  - `models.py` - Database models
  - `views.py` - View functions and classes
  - `forms.py` - Form definitions
  - `urls.py` - URL routing
  - `admin.py` - Admin interface configuration
  - `tests.py` - Unit tests
  - `templatetags/` - Custom template tags

- `templates/` - HTML templates
  - `base.html` - Base template
  - `blog/` - Blog-specific templates
  - `registration/` - Authentication templates

- `static/` - Static files (CSS, JavaScript)

## Features in Detail

### User Authentication
- Registration with extended profile (phone, DOB)
- Login/Logout functionality
- Password reset capability

### Blog Posts
- Create, Read, Update, Delete operations
- Password protection option
- Rich text content
- Pagination (5 posts per page)

### Interactive Polls
- Add polls to blog posts
- Multiple options support
- Real-time voting system

### Comments
- Add comments to blog posts
- Comment moderation in admin
- Nested display

## Testing

Run the test suite:
```bash
python manage.py test
```

## Deployment

The project is configured for Microsoft Azure deployment:

1. Create an Azure Web App
2. Configure environment variables
3. Set up database
4. Deploy using Azure CLI or GitHub Actions

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
