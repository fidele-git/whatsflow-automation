#!/bin/bash
# Database initialization script for production

echo "Initializing WhatsFlow database..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database tables created successfully!')"

# Run pricing initialization
python init_pricing.py

echo "Database initialization complete!"
echo "Next step: Create an admin user with scripts/create_admin.py"
