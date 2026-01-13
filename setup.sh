#!/bin/bash

echo "🚀 EduRate - Setting up the project..."
echo ""

# Check if Django is installed
if ! python3 -c "import django" 2>/dev/null; then
    echo "❌ Django is not installed."
    echo "Please run: pip install django pillow"
    exit 1
fi

echo "✅ Django is installed"
echo ""

# Run migrations
echo "📦 Running migrations..."
python3 manage.py makemigrations accounts courses ratings
python3 manage.py migrate

echo ""
echo "✅ Database migrations completed"
echo ""

# Create superuser prompt
echo "👤 Create a superuser account (admin panel access)"
echo "You can skip this and create it later with: python3 manage.py createsuperuser"
read -p "Do you want to create a superuser now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 manage.py createsuperuser
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎉 You can now run the development server:"
echo "   python3 manage.py runserver"
echo ""
echo "📝 Access the application at: http://localhost:8000"
echo "🔧 Admin panel: http://localhost:8000/admin"
echo ""
