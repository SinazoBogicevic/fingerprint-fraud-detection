#!/bin/bash
echo "🚀 Setting up fingerprint-fraud-detection project..."

# Check if virtual environment exists
if [ ! -d "local" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv local
fi

echo "✅ Activating virtual environment..."
source local/bin/activate

echo "📦 Installing requirements..."
pip install -r requirements.txt

echo "�� Installing test dependencies..."
pip install pytest pytest-cov httpx pytest-asyncio

echo "✅ Setup complete! Virtual environment is active."
echo "Run 'deactivate' when you're done."