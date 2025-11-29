# WhatsFlow Automation

A professional WhatsApp automation service platform built with Flask. This application provides a complete solution for businesses to automate their WhatsApp communications with features including pricing management, lead tracking, and admin dashboard.

## Features

- 🎯 **Dynamic Pricing Calculator** - Customizable pricing plans with discount management
- 📊 **Admin Dashboard** - Comprehensive analytics and lead management
- 📧 **Email Notifications** - Automatic notifications for new submissions
- 📤 **Export Functionality** - Export leads in multiple formats (CSV, Excel, PDF, Word, JSON)
- 🔐 **Secure Authentication** - Admin login with password hashing
- ⚙️ **Settings Management** - Change email and password from admin panel
- 🎨 **Modern UI** - Responsive design with professional aesthetics
- 🐳 **Docker Ready** - Easy deployment with Docker and Docker Compose

## Tech Stack

- **Backend**: Flask (Python 3.11)
- **Database**: SQLite (easily upgradable to PostgreSQL)
- **Authentication**: Flask-Login
- **Email**: Flask-Mail
- **Export**: openpyxl, reportlab, python-docx
- **Deployment**: Docker, Gunicorn

## Quick Start

### Prerequisites

- Python 3.11+
- pip
- (Optional) Docker and Docker Compose

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/fidele-git/whatsflow-automation.git
   cd whatsflow-automation
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   python init_pricing.py
   ```

6. **Create admin user**
   ```bash
   python scripts/create_admin.py
   ```

7. **Run the application**
   ```bash
   python app.py
   ```

   Visit `http://localhost:5000`

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Initialize database (first time only)**
   ```bash
   docker-compose exec web python init_pricing.py
   docker-compose exec web python scripts/create_admin.py
   ```

3. **View logs**
   ```bash
   docker-compose logs -f
   ```

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///whatsflow.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

## Project Structure

```
whatsflow-automation/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── config.py              # Configuration
├── init_pricing.py        # Pricing initialization
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── .env.example           # Environment variables template
├── static/                # Static files (CSS, JS, images)
├── templates/             # HTML templates
│   ├── admin/            # Admin panel templates
│   └── ...               # Public pages
├── scripts/               # Utility scripts
│   ├── init_db.sh        # Database initialization
│   └── create_admin.py   # Admin user creation
└── .github/
    └── workflows/         # GitHub Actions CI/CD
```

## Admin Panel

Access the admin panel at `/admin/login`

**Features:**
- Dashboard with lead statistics
- View and manage submissions
- Update pricing and discounts
- Export data in multiple formats
- Change email and password

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed production deployment instructions including:
- Server requirements
- SSL/HTTPS setup
- Database migration to PostgreSQL
- Environment configuration
- Security best practices

## Development

### Running Tests
```bash
# Install dev dependencies
pip install flake8 bandit

# Lint code
flake8 .

# Security check
bandit -r .
```

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is proprietary software. All rights reserved.

## Support

For support, email whatsappautomationbusiness@gmail.com

## Acknowledgments

- Built with Flask
- UI inspired by modern SaaS platforms
- Icons from Font Awesome
