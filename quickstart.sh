#!/bin/bash

# Quick Start Script for Driving Tracker
# This script helps you get started quickly

echo "🚗 Driving Tracker - Quick Start"
echo "================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo ""
    echo "Let's create it now..."
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: You need to edit .env with your Auth0 credentials"
    echo ""
    echo "Please complete these steps:"
    echo "1. Follow AUTH0_SETUP_GUIDE.md to get your Auth0 credentials"
    echo "2. Edit .env file and add:"
    echo "   - AUTH0_DOMAIN"
    echo "   - AUTH0_CLIENT_ID"
    echo "   - AUTH0_CLIENT_SECRET"
    echo ""
    echo "Then run this script again!"
    exit 1
fi

# Check if Auth0 credentials are set
source .env
if [ "$AUTH0_DOMAIN" = "your-tenant.us.auth0.com" ]; then
    echo "❌ Auth0 credentials not configured!"
    echo ""
    echo "Please edit .env file with your Auth0 credentials from:"
    echo "https://manage.auth0.com/dashboard/us/YOUR-TENANT/applications"
    echo ""
    echo "See AUTH0_SETUP_GUIDE.md for detailed instructions"
    exit 1
fi

echo "✅ .env file found and configured"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Initialize database
echo "🗄️  Initializing database..."
python3 -c "from database.models import db; db.create_tables(); print('✅ Database initialized')"
echo ""

# Ask what to run
echo "What would you like to run?"
echo ""
echo "1) Streamlit Dashboard only (port 8501)"
echo "2) Arduino API only (port 5000)"
echo "3) Both (Streamlit + API)"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting Streamlit Dashboard..."
        echo "📍 Open: http://localhost:8501"
        echo ""
        streamlit run app.py
        ;;
    2)
        echo ""
        echo "🚀 Starting Arduino API..."
        echo "📍 API available at: http://localhost:5000"
        echo ""
        python api_endpoint.py
        ;;
    3)
        echo ""
        echo "🚀 Starting both services..."
        echo "📍 Streamlit: http://localhost:8501"
        echo "📍 API: http://localhost:5000"
        echo ""
        echo "Opening Streamlit in new terminal..."
        osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && source venv/bin/activate && streamlit run app.py"'
        echo ""
        echo "Starting API in this terminal..."
        python api_endpoint.py
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
