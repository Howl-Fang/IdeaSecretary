#!/usr/bin/env python3
"""
Script to create test users and sample data for IdeaSecretary
"""

import os
import sys
from app import create_app
from models import db, User, IdeaBase, Idea
from services.auth_service import hash_password

def create_test_data():
    """Create test users and sample data"""
    app = create_app()
    
    with app.app_context():
        print("Creating test users and data...")
        
        # Create test user
        test_user = User(
            username='demo',
            email='demo@ideasecretary.local',
            password_hash=hash_password('demo123456'),
            openai_api_key='sk-test-key',
            openai_api_url='https://api.openai.com/v1',
            openai_model='gpt-3.5-turbo',
            language='en',
            dark_mode=False
        )
        
        db.session.add(test_user)
        db.session.commit()
        
        print(f"✓ Created test user: demo / demo123456")
        
        # Create default idea base
        default_base = IdeaBase(
            user_id=test_user.id,
            name='My Knowledge Base',
            description='Default knowledge base for organizing ideas',
            is_default=True
        )
        db.session.add(default_base)
        db.session.commit()
        
        print(f"✓ Created default idea base")
        
        # Create sample ideas
        sample_ideas = [
            {
                'title': 'Python Best Practices',
                'content': 'Always use virtual environments for Python projects. Follow PEP 8 style guide. Use type hints for better code clarity.',
                'tags': ['python', 'coding', 'best-practices']
            },
            {
                'title': 'Effective Note Taking',
                'content': 'Use Cornell method for taking notes. Review notes within 24 hours. Connect related ideas to form concept clusters.',
                'tags': ['productivity', 'learning', 'study-tips']
            },
            {
                'title': 'Web Development Workflow',
                'content': 'Set up proper development environment. Use version control from day one. Implement automated testing. Deploy early and often.',
                'tags': ['web-dev', 'devops', 'workflow']
            }
        ]
        
        for idx, idea_data in enumerate(sample_ideas, 1):
            idea = Idea(
                idea_base_id=default_base.id,
                title=idea_data['title'],
                content=idea_data['content'],
                tags=str(idea_data['tags']),
                order=idx
            )
            db.session.add(idea)
            default_base.idea_count += 1
            default_base.total_word_count += len(idea_data['content'].split())
        
        db.session.commit()
        
        print(f"✓ Created {len(sample_ideas)} sample ideas")
        
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
        
        print(f"✓ Created test user: alice / alice123456")
        
        print("\n✓ Test data created successfully!")
        print("\nTest Credentials:")
        print("  Demo User:")
        print("    Username: demo")
        print("    Password: demo123456")
        print("    Email: demo@ideasecretary.local")
        print("\n  Alice User:")
        print("    Username: alice")
        print("    Password: alice123456")
        print("    Email: alice@ideasecretary.local")

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
