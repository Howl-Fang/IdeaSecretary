# IdeaSecretary Development & Deployment Guide

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Running Tests](#running-tests)
3. [Creating Test Data](#creating-test-data)
4. [Backend Development](#backend-development)
5. [Frontend Development](#frontend-development)
6. [Deployment](#deployment)
7. [Troubleshooting](#troubleshooting)

## Local Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- SQLite3

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Initialize database (first run only)
python -c "from app import create_app; app = create_app(); print('Database initialized!')"

# Create test data (optional)
python create_test_data.py

# Run development server
python app.py
```

Backend will be available at `http://localhost:5000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local (optional, defaults to localhost:5000)
echo "REACT_APP_API_URL=http://localhost:5000/api" > .env.local

# Start development server
npm start
```

Frontend will be available at `http://localhost:3000`

## Running Tests

### Backend Tests

```bash
cd backend

# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_login
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test LoginPage.test.js
```

## Creating Test Data

```bash
cd backend
python create_test_data.py
```

**Default Test Credentials:**
- Demo User: `demo` / `demo123456`
- Alice User: `alice` / `alice123456`

## Backend Development

### Project Structure

```
backend/
├── app.py                 # Flask application factory
├── models.py              # SQLAlchemy ORM models
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── routes/
│   ├── auth.py           # Authentication endpoints
│   ├── ideas.py          # Idea management endpoints
│   ├── media.py          # Media upload/download
│   ├── user.py           # User settings and profile
│   ├── search.py         # Search functionality
│   └── ai.py             # AI-powered features
├── services/
│   ├── auth_service.py   # Authentication logic
│   ├── openai_service.py # OpenAI API integration
│   └── backup_service.py # Backup management
└── create_test_data.py   # Test data creation script
```

### Adding New Features

1. **Create Models** in `models.py`
2. **Create Services** in `services/` for business logic
3. **Create Routes** in `routes/` for API endpoints
4. **Register Routes** in `app.py`

### Database Migrations

```bash
# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade

# Revert migration
flask db downgrade
```

### API Response Format

All responses follow this format:

```json
{
  "data": { ... },
  "error": null,
  "status": 200
}
```

Errors:

```json
{
  "error": "Error message",
  "status": 400
}
```

## Frontend Development

### Project Structure

```
frontend/
├── public/
│   └── index.html        # HTML entry point
├── src/
│   ├── App.js            # Main app component
│   ├── index.js          # React entry point
│   ├── index.css         # Global styles
│   ├── pages/
│   │   ├── LoginPage.js  # Login/Register
│   │   ├── TreasuryPage.js
│   │   ├── IdeaBasePage.js
│   │   └── AccountPage.js
│   ├── components/       # Reusable components
│   ├── services/
│   │   └── api.js        # API client
│   ├── i18n/
│   │   └── i18n.js       # i18next configuration
│   └── styles/
│       └── App.css       # Component styles
└── package.json          # Dependencies
```

### Using the API Client

```javascript
import { ideasAPI, authAPI, userAPI } from '../services/api';

// Create idea
const response = await ideasAPI.createIdea(baseId, {
  title: 'My Idea',
  content: 'Idea content...',
  tags: ['tag1', 'tag2']
});

// Search
const results = await searchAPI.search('query', baseId);

// Update settings
await userAPI.updateSettings({ dark_mode: true });
```

### i18n Setup

Add new translations to `src/i18n/i18n.js`:

```javascript
const resources = {
  en: {
    translation: {
      'new.key': 'English text',
    },
  },
  zh: {
    translation: {
      'new.key': '中文文本',
    },
  },
};
```

Use in components:

```javascript
const { t } = useTranslation();
<h1>{t('new.key')}</h1>
```

## Deployment

### Production Build

#### Backend

```bash
cd backend

# Build Docker image (if using Docker)
docker build -t idea-secretary-backend .

# Or run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

#### Frontend

```bash
cd frontend

# Build for production
npm run build

# Output in: build/
```

### Docker Deployment

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
      SECRET_KEY: ${SECRET_KEY}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
    volumes:
      - ./backend/ideasecretary.db:/app/ideasecretary.db
      - ./backend/backups:/app/backups
      - ./backend/media_storage:/app/media_storage
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:5000/api
```

Run: `docker-compose up`

### Environment Variables

**Backend (.env)**
```
FLASK_ENV=production
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///ideasecretary.db
```

**Frontend (.env.local)**
```
REACT_APP_API_URL=https://api.example.com/api
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name example.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:5000/api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Media files
    location /media {
        alias /path/to/media_storage;
    }
}
```

## Troubleshooting

### Backend Issues

**Database locked error**
```bash
# Remove lock file
rm ideasecretary.db-journal

# Rebuild database
rm ideasecretary.db
python -c "from app import create_app; app = create_app()"
```

**Port already in use**
```bash
# On macOS/Linux
lsof -i :5000
kill -9 <PID>

# On Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Import errors**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Frontend Issues

**CORS errors**
- Ensure backend CORS is properly configured
- Check API URL in .env.local

**Blank page after login**
- Check browser console for errors
- Verify localStorage has access_token
- Check network tab for API calls

**Hot reload not working**
```bash
# Clear node_modules and reinstall
rm -rf node_modules
npm install
npm start
```

### General

**Can't connect frontend to backend**
1. Ensure backend is running on port 5000
2. Check `.env.local` has correct API URL
3. Verify CORS is enabled in Flask app
4. Check browser network tab for actual error

**Data not persisting**
1. Check database file exists: `ideasecretary.db`
2. Verify write permissions in backend directory
3. Check for database migration errors

## Performance Optimization

### Backend
- Implement query pagination for large datasets
- Add database indexing on frequently searched fields
- Use connection pooling for database

### Frontend
- Lazy load pages with React.lazy()
- Implement virtual scrolling for large lists
- Optimize images and assets

## Security Considerations

1. ✅ Use HTTPS in production
2. ✅ Rotate JWT secret regularly
3. ✅ Validate all user inputs server-side
4. ✅ Use CORS whitelist in production
5. ✅ Keep dependencies updated
6. ✅ Use environment variables for secrets
7. ✅ Implement rate limiting on APIs
8. ✅ Sanitize user content

## Monitoring & Logging

### Backend
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Event occurred")
logger.error("Error occurred")
```

### Frontend
```javascript
console.log('Log message');
console.error('Error occurred');
```

Monitor logs in production:
- CloudWatch (AWS)
- StackDriver (GCP)
- Azure Monitor
- ELK Stack (self-hosted)

## Next Steps

1. Deploy to cloud platform (AWS, GCP, Heroku, etc.)
2. Setup CI/CD pipeline (GitHub Actions, GitLab CI, etc.)
3. Configure monitoring and alerting
4. Implement advanced features:
   - Voice input with Web Speech API
   - Real-time sync with WebSockets
   - Collaborative features
   - Mobile app with React Native

For more information, see [README.md](./README.md)
