#!/bin/bash

# Resume Optimization Backend Startup Script

echo "🚀 Starting Resume Optimization Backend..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file and add your GEMINI_API_KEY"
    echo "   Then run this script again."
    exit 1
fi

# Check if GEMINI_API_KEY is set
if ! grep -q "GEMINI_API_KEY=your_gemini_api_key_here" .env; then
    echo "✅ Environment configuration found"
else
    echo "❌ Please set your GEMINI_API_KEY in the .env file"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "📦 Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🔧 Validating configuration..."
python -c "from src.config import Config; Config.validate_config(); print('✅ Configuration valid')"

echo "🌐 Starting server..."
echo "   API will be available at: http://localhost:8000"
echo "   API docs will be available at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py