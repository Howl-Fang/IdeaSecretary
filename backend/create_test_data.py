#!/usr/bin/env python3
"""
Script to create test users and sample data for IdeaSecretary
"""

import os
import sys
from app import create_app
from models import db, User, IdeaBase, Idea
from services.auth_service import hash_password

def create_demo_user_with_rich_data():
    """Create demo user with multiple bases and hierarchical content"""
    
    # Create demo user
    demo_user = User(
        username='demo',
        email='demo@ideasecretary.local',
        password_hash=hash_password('demo123456'),
        openai_api_key='sk-test-key',
        openai_api_url='https://api.openai.com/v1',
        openai_model='gpt-3.5-turbo',
        language='en',
        dark_mode=False
    )
    
    db.session.add(demo_user)
    db.session.commit()
    
    print(f"✓ Created demo user: demo / demo123456")
    
    # ========== IDEA BASE 1: My Knowledge Base ==========
    base1 = IdeaBase(
        user_id=demo_user.id,
        name='My Knowledge Base',
        description='Default knowledge base for organizing ideas',
        is_default=True
    )
    db.session.add(base1)
    db.session.commit()
    
    # Parent idea
    idea1_1 = Idea(
        idea_base_id=base1.id,
        title='Python Development',
        content='# Python Best Practices\n\n- Use virtual environments for all projects\n- Follow PEP 8 style guide\n- Use type hints for better code clarity\n- Write comprehensive docstrings\n- Test-driven development approach',
        tags='["python", "coding", "best-practices"]',
        order=1
    )
    db.session.add(idea1_1)
    db.session.commit()
    
    # Child ideas
    idea1_1_1 = Idea(
        idea_base_id=base1.id,
        parent_id=idea1_1.id,
        title='Virtual Environments',
        content='## Setting Up Virtual Environments\n\n```bash\npython3 -m venv venv\nsource venv/bin/activate\npip install -r requirements.txt\n```\n\nAlways use venv to isolate project dependencies and avoid version conflicts.',
        tags='["python", "setup", "environment"]',
        order=1
    )
    db.session.add(idea1_1_1)
    
    idea1_1_2 = Idea(
        idea_base_id=base1.id,
        parent_id=idea1_1.id,
        title='Type Hints & Documentation',
        content='## Using Type Hints\n\n```python\nfrom typing import List, Optional, Dict\n\ndef process_data(items: List[str]) -> Dict[str, int]:\n    """Process items and return statistics."""\n    return {item: len(item) for item in items}\n```\n\nType hints improve code clarity and enable better IDE support.',
        tags='["python", "typing", "documentation"]',
        order=2
    )
    db.session.add(idea1_1_2)
    db.session.commit()
    
    # Another parent idea
    idea1_2 = Idea(
        idea_base_id=base1.id,
        title='Effective Note Taking',
        content='# Note Taking Strategies\n\n## Cornell Method\n- Divide page into notes, cues, and summary sections\n- Review notes within 24 hours for better retention\n- Connect related ideas to form concept clusters\n\n## Active Learning\n- Engage with material during learning\n- Ask questions and seek clarification\n- Teach concepts to others',
        tags='["productivity", "learning", "study-tips"]',
        order=2
    )
    db.session.add(idea1_2)
    db.session.commit()
    
    idea1_2_1 = Idea(
        idea_base_id=base1.id,
        parent_id=idea1_2.id,
        title='Review Schedule',
        content='## Spaced Repetition Timeline\n\n- Review 1: After 1 day\n- Review 2: After 3 days\n- Review 3: After 7 days\n- Review 4: After 14 days\n- Review 5: After 30 days\n\nThis spacing optimizes long-term retention.',
        tags='["learning", "memory", "review"]',
        order=1
    )
    db.session.add(idea1_2_1)
    db.session.commit()
    
    # ========== IDEA BASE 2: Learning Projects ==========
    base2 = IdeaBase(
        user_id=demo_user.id,
        name='Learning Projects',
        description='Track ongoing learning projects and course progress'
    )
    db.session.add(base2)
    db.session.commit()
    
    idea2_1 = Idea(
        idea_base_id=base2.id,
        title='Web Development Mastery',
        content='# Full Stack Development Learning Path\n\n## Current Progress: 60%\n\n### Completed\n- HTML5 Fundamentals ✓\n- CSS3 & Responsive Design ✓\n- JavaScript Basics ✓\n- React Fundamentals ✓\n\n### In Progress\n- Advanced React Patterns\n- Node.js & Express\n- Database Design\n\n### TODO\n- Authentication & Security\n- Testing & Deployment\n- Performance Optimization',
        tags='["learning", "web-dev", "full-stack"]',
        order=1
    )
    db.session.add(idea2_1)
    db.session.commit()
    
    idea2_1_1 = Idea(
        idea_base_id=base2.id,
        parent_id=idea2_1.id,
        title='React Advanced Patterns',
        content='## Key Concepts to Master\n\n1. **Hooks Deep Dive**\n   - useReducer for complex state\n   - useContext for prop drilling\n   - Custom hooks creation\n\n2. **Performance Optimization**\n   - Memoization (React.memo, useMemo)\n   - Code splitting & lazy loading\n   - Bundle size analysis\n\n3. **State Management**\n   - Redux patterns\n   - Context API limitations\n   - Zustand as alternative',
        tags='["react", "advanced", "patterns"]',
        order=1
    )
    db.session.add(idea2_1_1)
    
    idea2_1_2 = Idea(
        idea_base_id=base2.id,
        parent_id=idea2_1.id,
        title='Backend with Node.js',
        content='## Express.js Fundamentals\n\n### Middleware Pipeline\n- Request -> Middleware -> Handler -> Response\n- Error handling middleware\n- Authentication middleware\n\n### RESTful API Design\n- Resource-based URLs\n- HTTP methods semantics\n- Status codes best practices\n- API versioning strategies',
        tags='["nodejs", "express", "backend"]',
        order=2
    )
    db.session.add(idea2_1_2)
    db.session.commit()
    
    idea2_2 = Idea(
        idea_base_id=base2.id,
        title='Machine Learning Basics',
        content='# ML Learning Journey\n\n## Foundations\n- Linear Algebra: vectors, matrices, operations\n- Statistics: distributions, probability, hypothesis testing\n- Calculus: derivatives, gradients, optimization\n\n## Supervised Learning\n- Linear Regression\n- Logistic Regression\n- Decision Trees & Random Forests\n- Support Vector Machines\n\n## Next: Unsupervised Learning & Neural Networks',
        tags='["machine-learning", "ai", "data-science"]',
        order=2
    )
    db.session.add(idea2_2)
    db.session.commit()
    
    # ========== IDEA BASE 3: Project Ideas ==========
    base3 = IdeaBase(
        user_id=demo_user.id,
        name='Project Ideas',
        description='Brainstorm and plan future projects'
    )
    db.session.add(base3)
    db.session.commit()
    
    idea3_1 = Idea(
        idea_base_id=base3.id,
        title='AI Chatbot for Documentation',
        content='# Project: Documentation AI Assistant\n\n## Objective\nBuild an AI chatbot that can answer questions about technical documentation\n\n## Tech Stack\n- Python Flask backend\n- React frontend\n- OpenAI API for NLP\n- Vector database for embeddings\n- PostgreSQL for data storage\n\n## Features\n- Real-time chat interface\n- Context-aware responses\n- Multi-language support\n- Citation tracking\n- Feedback mechanism\n\n## Timeline\n- Week 1-2: Setup & MVP\n- Week 3-4: AI Integration\n- Week 5-6: Polish & Deploy',
        tags='["project", "ai", "chatbot"]',
        order=1
    )
    db.session.add(idea3_1)
    db.session.commit()
    
    idea3_1_1 = Idea(
        idea_base_id=base3.id,
        parent_id=idea3_1.id,
        title='MVP Features',
        content='## Minimum Viable Product\n\n1. **Core Chat**\n   - Text input/output\n   - Simple prompt template\n   - Basic error handling\n\n2. **Documentation Loading**\n   - Upload markdown files\n   - Parse and index content\n   - Simple search\n\n3. **User Interface**\n   - Clean, minimal design\n   - Responsive layout\n   - Mobile-friendly',
        tags='["mvp", "features", "planning"]',
        order=1
    )
    db.session.add(idea3_1_1)
    db.session.commit()
    
    idea3_2 = Idea(
        idea_base_id=base3.id,
        title='Personal Finance Dashboard',
        content='# Project: Finance Dashboard\n\n## Goals\n- Track income and expenses\n- Visualize spending patterns\n- Budget planning and alerts\n- Investment portfolio tracking\n\n## Technology\n- Django backend with REST API\n- React dashboard with charts\n- PostgreSQL database\n- JWT authentication\n\n## Key Features\n- Multi-account support\n- Transaction categorization\n- Recurring expense tracking\n- Monthly/yearly reports\n- Export to CSV/PDF',
        tags='["project", "finance", "dashboard"]',
        order=2
    )
    db.session.add(idea3_2)
    db.session.commit()
    
    # Count all ideas and words
    all_ideas = Idea.query.filter_by(idea_base_id=base1.id).all()
    word_count1 = sum(len(i.content.split()) for i in all_ideas)
    base1.idea_count = len(all_ideas)
    base1.total_word_count = word_count1
    
    all_ideas = Idea.query.filter_by(idea_base_id=base2.id).all()
    word_count2 = sum(len(i.content.split()) for i in all_ideas)
    base2.idea_count = len(all_ideas)
    base2.total_word_count = word_count2
    
    all_ideas = Idea.query.filter_by(idea_base_id=base3.id).all()
    word_count3 = sum(len(i.content.split()) for i in all_ideas)
    base3.idea_count = len(all_ideas)
    base3.total_word_count = word_count3
    
    db.session.commit()
    
    print(f"✓ Created 3 idea bases with rich hierarchical content")
    print(f"  - My Knowledge Base: {base1.idea_count} ideas, {base1.total_word_count} words")
    print(f"  - Learning Projects: {base2.idea_count} ideas, {base2.total_word_count} words")
    print(f"  - Project Ideas: {base3.idea_count} ideas, {base3.total_word_count} words")
    
    return demo_user

def create_test_data():
    """Create test users and sample data"""
    app = create_app()
    
    with app.app_context():
        print("Creating test users and data...\n")
        
        # Create demo user with rich data
        demo_user = create_demo_user_with_rich_data()
        
        # Create another test user
        test_user2 = User(
            username='alice',
            email='alice@ideasecretary.local',
            password_hash=hash_password('alice123456'),
            language='zh',
            dark_mode=True
        )
        
        db.session.add(test_user2)
        db.session.commit()
        
        print(f"✓ Created test user: alice / alice123456\n")
        
        print("✓ Test data created successfully!\n")
        print("=" * 50)
        print("Test Credentials:")
        print("=" * 50)
        print("\n  Demo User:")
        print("    Username: demo")
        print("    Password: demo123456")
        print("    Email: demo@ideasecretary.local")
        print("    \n    Features:")
        print("    - 3 idea bases with 12+ ideas")
        print("    - Hierarchical idea structure")
        print("    - Rich markdown content")
        print("    - OpenAI integration ready")
        print("\n  Alice User:")
        print("    Username: alice")
        print("    Password: alice123456")
        print("    Email: alice@ideasecretary.local")
        print("=" * 50)

if __name__ == '__main__':
    # Check if database exists and has data
    db_path = 'ideasecretary.db'
    
    if os.path.exists(db_path):
        response = input(f"Database {db_path} already exists. Delete it? (y/n): ")
        if response.lower() == 'y':
            os.remove(db_path)
            create_test_data()
        else:
            print("Skipped.")
    else:
        create_test_data()
