from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    """
    Represents a user in the system.

    Fields:
    - id (UUID/Integer): Unique identifier for the user
    - username (String): User's username
    - email (String): User's email address
    - timezone (String): User's preferred timezone (e.g., "America/New_York")
    - created_at (DateTime): Timestamp when the user was created
    - updated_at (DateTime): Timestamp when the user was last updated
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    timezone = Column(String, nullable=False, default="UTC")  # Default to UTC
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    tasks = relationship("Task", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"