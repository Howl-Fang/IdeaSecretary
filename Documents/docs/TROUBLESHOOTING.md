# IdeaSecretary Troubleshooting Guide

## Common Issues and Solutions

### 1. Frontend Error: `Error: spawn react-scripts ENOENT`

**Symptoms:**
```
Error: spawn react-scripts ENOENT
at ChildProcess._handle.onexit (node:internal/child_process:286:19)
```

**Cause:**
The `react-scripts` package is not properly installed or the version in `package.json` is invalid.

**Solution:**

```bash
cd frontend
# Option 1: Clean reinstall (recommended)
rm -rf node_modules package-lock.json
npm install

# Option 2: If still failing, verify package.json
# Ensure react-scripts version is: "react-scripts": "5.0.1"
# NOT: "react-scripts": "^0.0.0"
```

**Prevention:**
- Always verify package.json has valid dependency versions
- Use `npm install` after pulling code changes
- Don't commit broken node_modules; rely on package-lock.json

---

### 2. Frontend Error: `Error: spawn /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe ENOENT` (WSL)

**Symptoms:**
PowerShell executable not found when running `npm start` in WSL.

**Cause:**
React Scripts tries to launch a browser using Windows paths that don't exist in WSL.

**Solution:**

Already fixed in the current codebase! The solution includes:
- Added `cross-env` package
- Set `BROWSER=none` environment variable in npm scripts
- Package.json line 22: `"start": "cross-env BROWSER=none react-scripts start"`

**Manual Fix (if reverting):**
```bash
cd frontend
npm install cross-env
# Update package.json scripts.start to:
# "start": "cross-env BROWSER=none react-scripts start"
```

---

### 3. Backend Error: `ModuleNotFoundError: No module named 'flask'`

**Symptoms:**
```
ModuleNotFoundError: No module named 'flask'
```

**Cause:**
Python dependencies are not installed.

**Solution:**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Verify:**
```bash
python3 -c "import flask; print('Flask installed')"
```

---

### 4. Database Error: `OperationalError: unable to open database file`

**Symptoms:**
```
OperationalError: unable to open database file
```

**Cause:**
- Database directory doesn't exist
- Insufficient permissions
- Incorrect database path

**Solution:**

```bash
cd backend
# Create instance directory if it doesn't exist
mkdir -p instance

# Reinitialize database
source .venv/bin/activate
python3 create_test_data.py  # Say 'y' to delete and recreate
```

**Verify:**
```bash
ls -la instance/ideasecretary.db
```

---

### 5. Frontend Blank Page / Nothing Renders

**Symptoms:**
- Browser shows blank page
- No console errors
- Network requests working

**Cause:**
- App.js not found
- Public/index.html issues
- Missing CSS files

**Solution:**

```bash
cd frontend
# Verify App.js exists
ls src/App.js
ls src/App.css

# Check public/index.html
ls public/index.html

# Rebuild if necessary
npm run build

# Clear browser cache and hard refresh (Ctrl+Shift+R)
```

---

### 6. API Connection Error: `ERR_CONNECTION_REFUSED`

**Symptoms:**
```
GET http://localhost:5000/api/... failed
ERR_CONNECTION_REFUSED
```

**Cause:**
Backend server is not running.

**Solution:**

```bash
# Terminal 1: Start backend
cd backend
source .venv/bin/activate
python3 app.py

# Expected output:
# WARNING in app.run() is not recommended for production use.
# Use a production WSGI server instead.
# Running on http://127.0.0.1:5000
```

**Verify:**
```bash
curl http://localhost:5000/api/health
# Should return: {"status": "ok"}
```

---

### 7. Port Already in Use

**Symptoms:**
```
ERROR: Address already in use
Port 5000 or 3000 already in use
```

**Cause:**
Another application is using the same port.

**Solution:**

**Option 1: Kill the process**
```bash
# Find process using port 5000 (backend)
lsof -i :5000
# Kill it: kill -9 <PID>

# Find process using port 3000 (frontend)
lsof -i :3000
# Kill it: kill -9 <PID>
```

**Option 2: Change port**
```bash
# Backend: Edit backend/config.py
# Change: FLASK_PORT = 5000 to FLASK_PORT = 5001

# Frontend: Edit frontend/.env.local
# Change: REACT_APP_API_URL=http://localhost:5000/api
# to: REACT_APP_API_URL=http://localhost:5001/api
```

---

### 8. Docker Build Fails

**Symptoms:**
```
docker-compose build
... fails with various errors
```

**Cause:**
- Outdated Docker images
- Missing dependencies
- Cache issues

**Solution:**

```bash
# Clean rebuild (no cache)
docker-compose build --no-cache

# If still failing, remove old containers
docker-compose down -v

# Rebuild from scratch
docker-compose up --build
```

---

### 9. Docker Container Exits Immediately

**Symptoms:**
```
docker-compose up
... service "backend" exited with code 1
```

**Cause:**
- Application error
- Missing environment variables
- Database initialization failed

**Solution:**

```bash
# View logs
docker-compose logs backend
docker-compose logs frontend

# Check environment variables
cat .env  # backend .env file
```

---

### 10. Test Data Not Loading

**Symptoms:**
- Demo user doesn't exist
- No sample ideas in database
- Login fails with demo credentials

**Cause:**
`create_test_data.py` not run or failed.

**Solution:**

```bash
cd backend
source .venv/bin/activate

# Run data creation
python3 create_test_data.py

# When prompted "Database ... already exists. Delete it? (y/n):"
# Type: y

# Expected output:
# ✓ Created demo user: demo / demo123456
# ✓ Created 3 idea bases with rich hierarchical content
# ✓ Test data created successfully!
```

**Verify:**
```bash
# Check database directly
sqlite3 instance/ideasecretary.db
sqlite> SELECT username FROM users;
# Should show: demo, alice
```

---

### 11. Login Fails

**Symptoms:**
- Login page stuck
- Invalid credentials error
- 401 Unauthorized response

**Cause:**
- Wrong credentials
- Backend not running
- JWT token issues

**Solution:**

```bash
# Verify credentials (should be exactly):
# Username: demo
# Password: demo123456
# Email: demo@ideasecretary.local

# Verify backend is running:
curl http://localhost:5000/api/health

# Check browser console for errors
# Check backend logs for exceptions
```

---

### 12. Slow Performance

**Symptoms:**
- Pages load slowly
- API responses delayed
- High CPU/memory usage

**Cause:**
- Large dataset
- Missing indexes
- Resource-heavy operations

**Solution:**

```bash
# Frontend optimization
cd frontend
npm run build  # Creates optimized production build

# Backend optimization
# Use production server (Gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Database optimization
# Create indexes if needed (SQLAlchemy ORM handles this)

# Monitor resource usage
top  # Linux
```

---

## General Troubleshooting Steps

### 1. Check Logs
```bash
# Backend logs
# Usually in console where app is running

# Frontend logs
# Browser console (F12 Developer Tools)
# Check Application > Local Storage for tokens

# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 2. Verify Installation
```bash
# Backend
python3 --version  # Should be 3.8+
source venv/bin/activate
pip list  # Check if flask, sqlalchemy installed

# Frontend
node --version  # Should be 14+
npm --version  # Should be 6+
npm list react  # Check React installed
```

### 3. Clear Caches
```bash
# Frontend cache
cd frontend
rm -rf node_modules package-lock.json build dist
npm install

# Backend cache
cd backend
find . -type d -name __pycache__ -exec rm -rf {} +
find . -name "*.pyc" -delete
```

### 4. Database Reset
```bash
cd backend
rm -f instance/ideasecretary.db
python3 create_test_data.py  # Recreate from scratch
```

### 5. Browser Cache
- Hard refresh: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
- Clear Local Storage: F12 → Application → Local Storage → Clear All

---

## Quick Commands Reference

```bash
# Frontend
cd frontend && npm start                # Start dev server
cd frontend && npm run build            # Production build
cd frontend && npm install              # Install dependencies
cd frontend && npm test                 # Run tests

# Backend
cd backend && source .venv/bin/activate # Activate venv
cd backend && pip install -r requirements.txt  # Install deps
cd backend && python3 app.py            # Start server
cd backend && python3 create_test_data.py     # Load demo data

# Docker
docker-compose up                       # Start all services
docker-compose down                     # Stop all services
docker-compose build                    # Build images
docker-compose logs -f                  # View logs

# Database
sqlite3 instance/ideasecretary.db       # Open database
.tables                                 # List tables
SELECT * FROM users;                    # Query users
```

---

## When to Clear vs. Reinstall

### Clear Cache (Fast)
- Browser not displaying updates
- Frontend styles not applying
- Minor local storage issues

```bash
# Browser DevTools → Clear Site Data
# Or: Ctrl+Shift+Delete
```

### Reinstall Dependencies (Medium)
- New package added to package.json
- Strange import errors
- Version mismatches

```bash
cd frontend && rm -rf node_modules package-lock.json && npm install
cd backend && pip install -r requirements.txt
```

### Full System Reset (Slow but thorough)
- Multiple issues
- Database corruption
- Major version conflicts

```bash
# Frontend
cd frontend && rm -rf node_modules package-lock.json build dist && npm install && npm start

# Backend
cd backend && rm -rf .venv instance/*.db && python3 -m venv venv && \
source venv/bin/activate && pip install -r requirements.txt && \
python3 create_test_data.py && python3 app.py

# Docker
docker-compose down -v && docker-compose up --build
```

---

## Getting Help

1. **Check logs first** - Most errors are clearly described in terminal output
2. **Read error messages carefully** - They usually point to the exact issue
3. **Review this guide** - Most common issues are listed above
4. **Check documentation** - README.md, DEVELOPMENT.md, DEMO_DATA.md
5. **Review code comments** - Implementation details are documented inline

---

## Known Limitations

1. **SQLite limitations** - For production, migrate to PostgreSQL
2. **Single machine deployment** - Scaling requires database and session management changes
3. **No real-time sync** - Future enhancement can add WebSocket support
4. **Voice and OCR** - UI ready but not yet implemented

---

*Last Updated: 2026-04-10*
*Version: 0.1.0-MVP*
