"""Database models for driving tracker application."""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class User(Base):
    """User model for storing user information and relationships."""
    __tablename__ = 'users'

    id = Column(String, primary_key=True)  # Auth0 user ID
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    role = Column(String, default='driver')  # 'supervisor' or 'driver'
    supervisor_id = Column(String, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    supervisor = relationship('User', remote_side=[id], backref='supervised_drivers')
    driving_sessions = relationship('DrivingSession', back_populates='driver', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


class DrivingSession(Base):
    """Model for individual driving sessions."""
    __tablename__ = 'driving_sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    driver_id = Column(String, ForeignKey('users.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    distance = Column(Float, default=0.0)  # in kilometers
    duration = Column(Integer, default=0)  # in seconds
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    driver = relationship('User', back_populates='driving_sessions')
    metrics = relationship('DrivingMetric', back_populates='session', cascade='all, delete-orphan')
    events = relationship('DrivingEvent', back_populates='session', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<DrivingSession {self.id} - Driver: {self.driver_id}>"


class DrivingMetric(Base):
    """Model for real-time driving metrics from Arduino."""
    __tablename__ = 'driving_metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('driving_sessions.id'), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Arduino sensor data
    speed = Column(Float, default=0.0)  # km/h
    acceleration = Column(Float, default=0.0)  # m/s²
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    heading = Column(Float, nullable=True)  # degrees

    # Additional metrics
    rpm = Column(Integer, nullable=True)
    fuel_level = Column(Float, nullable=True)
    engine_temp = Column(Float, nullable=True)

    # Relationships
    session = relationship('DrivingSession', back_populates='metrics')

    def __repr__(self):
        return f"<DrivingMetric {self.id} - Speed: {self.speed} km/h>"


class DrivingEvent(Base):
    """Model for driving events (harsh braking, speeding, etc.)."""
    __tablename__ = 'driving_events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('driving_sessions.id'), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    event_type = Column(String, nullable=False)  # 'harsh_brake', 'harsh_acceleration', 'speeding', etc.
    severity = Column(String, default='low')  # 'low', 'medium', 'high'
    description = Column(Text, nullable=True)

    # Event-specific data
    speed_at_event = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Relationships
    session = relationship('DrivingSession', back_populates='events')

    def __repr__(self):
        return f"<DrivingEvent {self.event_type} - Severity: {self.severity}>"


class Database:
    """Database connection and session manager."""

    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or os.getenv('DATABASE_URL', 'sqlite:///driving_tracker.db')
        self.engine = create_engine(self.database_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Create all database tables."""
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """Get a new database session."""
        return self.SessionLocal()

    def get_or_create_user(self, auth0_user: dict) -> User:
        """Get or create a user from Auth0 user info."""
        session = self.get_session()
        try:
            user_id = auth0_user.get('sub') or auth0_user.get('user_id')
            user = session.query(User).filter_by(id=user_id).first()

            if not user:
                user = User(
                    id=user_id,
                    email=auth0_user.get('email'),
                    name=auth0_user.get('name'),
                    role=auth0_user.get('role', 'driver'),
                    supervisor_id=auth0_user.get('supervisor_id')
                )
                session.add(user)
                session.commit()
            else:
                # Update user info
                user.email = auth0_user.get('email', user.email)
                user.name = auth0_user.get('name', user.name)
                user.role = auth0_user.get('role', user.role)
                user.supervisor_id = auth0_user.get('supervisor_id', user.supervisor_id)
                session.commit()

            return user
        finally:
            session.close()

    def get_supervised_drivers(self, supervisor_id: str) -> List[User]:
        """Get all drivers supervised by a supervisor."""
        session = self.get_session()
        try:
            drivers = session.query(User).filter_by(supervisor_id=supervisor_id).all()
            return drivers
        finally:
            session.close()


# Global database instance
db = Database()
