#!/bin/bash

# Setup script for IdeaSecretary backend

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p ../data/media
mkdir -p ../data/media_trash
mkdir -p ../data/backups

# Create environment file
cat > .env << EOF
# Flask Configuration
FLASK_ENV=development
FLASK_APP=run.py
PORT=5000

# Database Configuration
DATABASE_URL=sqlite:////Users/lihaofang/Documents/IdeaSecretary/data/idea_secretary.db

# OpenAI Configuration (User will set these)
OPENAI_API_KEY=
OPENAI_API_BASE=https://api.openai.com/v1

# Security
SECRET_KEY=your-secret-key-change-in-production
EOF

echo "Backend setup complete!"
echo "To start the development server, run: source .venv/bin/activate && python run.py"
