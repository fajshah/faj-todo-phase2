#!/usr/bin/env python3
"""
Script to manually create a test user in the database
"""
import asyncio
import uuid
from datetime import datetime
from sqlmodel import SQLModel, create_engine, Session
from src.models.user import User
from src.auth.hashing import hash_password

# Use the sync engine to create a test user
from src.database.engine import sync_engine

def create_test_user():
    # Create a test user directly in the database
    with Session(sync_engine) as session:
        # Check if user already exists by email (not by ID)
        existing_user = session.query(User).filter(User.email == "test@example.com").first()

        if existing_user:
            print("Test user already exists")
            return existing_user.id

        # Create new user
        user_id = uuid.uuid4()
        user = User(
            id=user_id,
            email="test@example.com",
            password_hash=hash_password("password123"),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        print(f"Created test user with ID: {user.id}")
        return user.id

if __name__ == "__main__":
    user_id = create_test_user()
    print(f"Test user created successfully with ID: {user_id}")