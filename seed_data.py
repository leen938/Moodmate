#!/usr/bin/env python3
"""
Data seeding script for MoodMate
Run this to populate the database with sample data for testing
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def create_user_and_get_token(username, password):
    """Create a user and return the auth token"""
    response = requests.post(f"{BASE_URL}/user/init", json={
        "username": username,
        "password": password
    })
    
    if response.status_code == 200:
        data = response.json()
        return data["data"]["token"]
    else:
        print(f"Failed to create user {username}: {response.text}")
        return None

def create_task(token, title, description, priority, deadline=None):
    """Create a task for the authenticated user"""
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": title,
        "description": description,
        "priority": priority
    }
    if deadline:
        data["deadline"] = deadline
    
    response = requests.post(f"{BASE_URL}/tasks/", json=data, headers=headers)
    
    if response.status_code == 200:
        print(f"✅ Created task: {title}")
        return True
    else:
        print(f"❌ Failed to create task {title}: {response.text}")
        return False

def main():
    print("🌱 Seeding MoodMate database with sample data...")
    
    # Sample users and their tasks
    users_data = [
        {
            "username": "alice@example.com",
            "password": "password123",
            "tasks": [
                {
                    "title": "Complete project proposal",
                    "description": "Write and submit the final project proposal for CMPS 279",
                    "priority": "HIGH",
                    "deadline": (datetime.now() + timedelta(days=3)).isoformat()
                },
                {
                    "title": "Study for midterm",
                    "description": "Review all course materials and practice problems",
                    "priority": "URGENT",
                    "deadline": (datetime.now() + timedelta(days=1)).isoformat()
                },
                {
                    "title": "Grocery shopping",
                    "description": "Buy ingredients for the week",
                    "priority": "LOW",
                    "deadline": (datetime.now() + timedelta(days=2)).isoformat()
                }
            ]
        },
        {
            "username": "bob@example.com", 
            "password": "password123",
            "tasks": [
                {
                    "title": "Fix bug in authentication",
                    "description": "Debug the login issue reported by users",
                    "priority": "HIGH",
                    "deadline": (datetime.now() + timedelta(days=1)).isoformat()
                },
                {
                    "title": "Update documentation",
                    "description": "Add API documentation for new endpoints",
                    "priority": "MEDIUM",
                    "deadline": (datetime.now() + timedelta(days=5)).isoformat()
                },
                {
                    "title": "Team meeting",
                    "description": "Weekly standup with development team",
                    "priority": "LOW",
                    "deadline": (datetime.now() + timedelta(days=1)).isoformat()
                }
            ]
        },
        {
            "username": "charlie@example.com",
            "password": "password123", 
            "tasks": [
                {
                    "title": "Design user interface",
                    "description": "Create mockups for the mobile app interface",
                    "priority": "MEDIUM",
                    "deadline": (datetime.now() + timedelta(days=4)).isoformat()
                },
                {
                    "title": "Code review",
                    "description": "Review pull requests from team members",
                    "priority": "HIGH",
                    "deadline": (datetime.now() + timedelta(days=1)).isoformat()
                }
            ]
        }
    ]
    
    # Create users and their tasks
    for user_data in users_data:
        print(f"\n👤 Creating user: {user_data['username']}")
        token = create_user_and_get_token(user_data['username'], user_data['password'])
        
        if token:
            print(f"📝 Adding {len(user_data['tasks'])} tasks...")
            for task in user_data['tasks']:
                create_task(token, **task)
        else:
            print(f"❌ Skipping tasks for {user_data['username']}")
    
    print("\n🎉 Database seeding complete!")
    print("\nYou can now test the API with these credentials:")
    for user_data in users_data:
        print(f"  - {user_data['username']} / {user_data['password']}")

if __name__ == "__main__":
    main()

