# Demo Data Guide for IdeaSecretary

This document describes the demo data that is pre-populated when you run `create_test_data.py`. The demo user account showcases key features of the system with realistic, hierarchical content.

## Demo User Account

**Username:** `demo`  
**Password:** `demo123456`  
**Email:** `demo@ideasecretary.local`

### Configured Settings
- **Language:** English
- **Dark Mode:** Disabled
- **OpenAI Model:** gpt-3.5-turbo
- **OpenAI API URL:** https://api.openai.com/v1

## Demo Data Structure

The demo user has **3 Idea Bases** with **12 total ideas** organized hierarchically:

### 📦 1. My Knowledge Base (Default)
**Description:** Default knowledge base for organizing ideas  
**Total Ideas:** 5 | **Total Words:** 193

This base demonstrates best practices for knowledge organization and study techniques.

#### Top-Level Ideas:
1. **Python Development** (Parent idea with 2 children)
   - 📝 Content: Python best practices and coding standards
   - Tags: `python`, `coding`, `best-practices`
   
   - **├─ Virtual Environments** (Child idea)
     - 📝 Step-by-step guide for setting up Python virtual environments
     - Includes code examples
     - Tags: `python`, `setup`, `environment`
   
   - **└─ Type Hints & Documentation** (Child idea)
     - 📝 Guide on using Python type hints for code clarity
     - Python code examples with typing module
     - Tags: `python`, `typing`, `documentation`

2. **Effective Note Taking** (Parent idea with 1 child)
   - 📝 Content: Cornell method and active learning strategies
   - Tags: `productivity`, `learning`, `study-tips`
   
   - **└─ Review Schedule** (Child idea)
     - 📝 Spaced repetition timeline for optimal retention
     - Based on scientifically-proven learning techniques
     - Tags: `learning`, `memory`, `review`

---

### 📦 2. Learning Projects
**Description:** Track ongoing learning projects and course progress  
**Total Ideas:** 4 | **Total Words:** 201

This base demonstrates project tracking and learning path planning.

#### Top-Level Ideas:
1. **Web Development Mastery** (Parent idea with 2 children)
   - 📝 Content: Full-stack development learning path with progress tracking
   - Shows: Completed topics (HTML, CSS, JS, React) + In Progress + TODO sections
   - Progress: 60% complete
   - Tags: `learning`, `web-dev`, `full-stack`
   
   - **├─ React Advanced Patterns** (Child idea)
     - 📝 Deep dive into advanced React concepts
     - Topics: Hooks, Performance Optimization, State Management
     - Tags: `react`, `advanced`, `patterns`
   
   - **└─ Backend with Node.js** (Child idea)
     - 📝 Express.js fundamentals and RESTful API design
     - Middleware patterns and API best practices
     - Tags: `nodejs`, `express`, `backend`

2. **Machine Learning Basics**
   - 📝 Content: ML learning journey outline
   - Covers: Linear Algebra, Statistics, Calculus, Supervised & Unsupervised Learning
   - Tags: `machine-learning`, `ai`, `data-science`
   - (No children - top-level topic)

---

### 📦 3. Project Ideas
**Description:** Brainstorm and plan future projects  
**Total Ideas:** 3 | **Total Words:** 188

This base demonstrates project planning and ideation workflows.

#### Top-Level Ideas:
1. **AI Chatbot for Documentation** (Parent idea with 1 child)
   - 📝 Content: Detailed project plan for an AI-powered documentation assistant
   - Includes: Objective, Tech Stack, Features, Timeline
   - Tech: Flask, React, OpenAI, Vector DB, PostgreSQL
   - Features: Real-time chat, context-aware responses, multi-language support, citation tracking
   - Tags: `project`, `ai`, `chatbot`
   
   - **└─ MVP Features** (Child idea)
     - 📝 Minimum viable product specification
     - Core Chat, Documentation Loading, User Interface
     - Tags: `mvp`, `features`, `planning`

2. **Personal Finance Dashboard**
   - 📝 Content: Finance tracking and visualization project
   - Goals: Expense tracking, Budget planning, Investment portfolio
   - Tech: Django, React, PostgreSQL
   - Features: Multi-account support, Categorization, Reports
   - Tags: `project`, `finance`, `dashboard`
   - (No children - single topic)

---

## Content Features Showcased

The demo data demonstrates the following system capabilities:

### 1. **Hierarchical Organization**
- Parent-child idea relationships showing how to organize related concepts
- Example: "Python Development" groups "Virtual Environments" and "Type Hints"

### 2. **Rich Markdown Content**
- Formatted text with headings, bold, code blocks
- Code examples in Python, Bash, and JavaScript
- Lists and structured layouts

### 3. **Tagging System**
- Multiple tags per idea for categorization
- Consistent tag naming conventions
- Example tags: `python`, `learning`, `web-dev`, `project`

### 4. **Realistic Use Cases**
- **Learning Tracking:** Shows progress on courses and skill development
- **Note Taking:** Demonstrates Cornell method and spaced repetition
- **Project Planning:** Contains detailed specs for hypothetical projects
- **Best Practices:** Covers coding standards and workflows

### 5. **Cross-Base Organization**
- Different bases for different purposes (Knowledge, Learning, Projects)
- Ability to manage multiple knowledge bases independently

---

## Using Demo Data

### Accessing Demo Features

1. **Login** with demo credentials:
   ```
   Username: demo
   Password: demo123456
   ```

2. **View Idea Bases:** Navigate to "My Idea Base" to see all 3 bases

3. **Explore Hierarchies:** Click on parent ideas to expand child ideas

4. **Search:** Use the search feature to find ideas by title or tags
   - Try: "python", "learning", "react", "project"

5. **Try AI Features:** 
   - The account has OpenAI configured (test key)
   - Try the "Organize", "Inspire", or "Summarize" features

### Modifying Demo Data

To reset the demo database with fresh data:

```bash
cd backend
source .venv/bin/activate
python3 create_test_data.py
# Select 'y' to delete and recreate the database
```

---

## Additional Test User

**Username:** `alice`  
**Password:** `alice123456`  
**Email:** `alice@ideasecretary.local`

This is a minimal test account with:
- Language set to Chinese (zh)
- Dark mode enabled
- No pre-populated idea bases (ready for custom data)

---

## Database Schema Verification

The demo data validates the following database schema:

```
Users
├── id (UUID)
├── username
├── email
├── password_hash (bcrypt)
└── openai_api_* (configuration)

IdeaBases
├── id (UUID)
├── user_id (foreign key)
├── name
├── description
├── idea_count (auto-updated)
└── total_word_count (auto-updated)

Ideas
├── id (UUID)
├── idea_base_id (foreign key)
├── parent_id (self-referencing for hierarchy)
├── title
├── content (markdown)
├── tags (JSON array)
├── order (display order)
└── timestamps
```

---

## Tips for Exploring

1. **Try Search:** Each base has tagged ideas. Use tags to find related content.

2. **View Statistics:** Check the "Account" page to see:
   - Total ideas: 12
   - Total knowledge bases: 3
   - Default language: English

3. **Test Hierarchy:** Expand parent ideas to see how child ideas are displayed

4. **Review Markdown:** Open individual ideas to see properly formatted markdown content

5. **Experiment with Tags:** The filter system (when implemented) will use these tags

---

## For Development & Testing

### Database Inspection

To inspect the demo database directly:

```bash
cd backend
sqlite3 instance/ideasecretary.db

# View all ideas
sqlite> SELECT id, title, parent_id FROM ideas LIMIT 20;

# View idea base statistics
sqlite> SELECT name, idea_count, total_word_count FROM idea_bases;

# Count ideas per base
sqlite> SELECT ib.name, COUNT(i.id) FROM idea_bases ib 
         LEFT JOIN ideas i ON i.idea_base_id = ib.id 
         GROUP BY ib.id;
```

### Running Tests

Use the demo account for manual testing:

```bash
# Start backend
cd backend && python3 app.py

# Start frontend (in another terminal)
cd frontend && npm start

# Login with demo credentials and test features
```

---

## Next Steps

After exploring the demo data, you can:

1. **Add Your Own Content:** Create new idea bases and ideas
2. **Configure OpenAI:** Update API key in Account settings
3. **Test AI Features:** Use real OpenAI API key to test organizing/inspiring features
4. **Export & Backup:** Test backup functionality
5. **Dark Mode:** Toggle dark mode from Account settings to see theme switching

---

*Demo data created and verified on 2026-04-10. Last updated: initialization script version 2.0*
