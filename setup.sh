#!/bin/bash

# AIZA Enterprise AI Platform - One-Command Setup
# Built with ❤️ by AIZA

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   AIZA Enterprise AI Platform - Setup Script             ║"
echo "║   Built with ❤️ by AIZA                                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Create environment file
echo "📝 Creating environment configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys before continuing"
    echo "   Required: OPENAI_API_KEY, ASSEMBLYAI_API_KEY, ELEVENLABS_API_KEY"
    read -p "Press Enter after updating .env file..."
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs data/uploads data/exports data/backups

# Build Docker images
echo "🐳 Building Docker images..."
docker-compose build

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Run database migrations
echo "🗄️  Running database migrations..."
docker-compose exec -T backend alembic upgrade head

# Create admin user
echo "👤 Creating admin user..."
docker-compose exec -T backend python scripts/create_admin.py

# Health check
echo "🏥 Performing health check..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
fi

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend health check failed"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   🎉 Setup Complete!                                      ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Access the platform:"
echo "   Dashboard:  http://localhost:3000"
echo "   API:        http://localhost:8000"
echo "   API Docs:   http://localhost:8000/docs"
echo "   Admin:      http://localhost:3000/admin"
echo ""
echo "📚 Next steps:"
echo "   1. Login with admin credentials (check logs above)"
echo "   2. Configure your AI services in Settings"
echo "   3. Start building amazing AI applications!"
echo ""
echo "📖 Documentation: https://docs.aiza.dev"
echo "💬 Support: support@aiza.dev"
echo ""
echo "Built with ❤️ by AIZA - Empowering AI Innovation"
