"""
SQLAlchemy ORM Models for InnovLead Education Bot
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from database.connection import Base


class User(Base):
    """User model - stores Telegram user information"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    language_code = Column(String(10), default='en')
    registration_date = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    consent_data_processing = Column(Boolean, default=False)
    
    # Relationships
    progress = relationship('UserProgress', back_populates='user', cascade='all, delete-orphan')
    interactions = relationship('Interaction', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"


class Module(Base):
    """Educational module model"""
    __tablename__ = 'modules'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    module_code = Column(String(50), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, nullable=True)
    total_lessons = Column(Integer, default=0)
    estimated_duration_minutes = Column(Integer, nullable=True)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    lessons = relationship('Lesson', back_populates='module', cascade='all, delete-orphan')
    progress = relationship('UserProgress', back_populates='module')
    
    def __repr__(self):
        return f"<Module(code={self.module_code}, title={self.title})>"


class Lesson(Base):
    """Individual lesson within a module"""
    __tablename__ = 'lessons'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    module_id = Column(Integer, ForeignKey('modules.id', ondelete='CASCADE'), nullable=False)
    lesson_code = Column(String(50), nullable=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    order_index = Column(Integer, nullable=True)
    has_quiz = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    module = relationship('Module', back_populates='lessons')
    progress = relationship('UserProgress', back_populates='lesson')
    
    def __repr__(self):
        return f"<Lesson(code={self.lesson_code}, title={self.title})>"


class UserProgress(Base):
    """Tracks user progress through modules and lessons (CRA impact tracking)"""
    __tablename__ = 'user_progress'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    module_id = Column(Integer, ForeignKey('modules.id', ondelete='CASCADE'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.id', ondelete='SET NULL'), nullable=True)
    status = Column(String(20), default='in_progress')  # 'in_progress', 'completed', 'skipped'
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    quiz_score = Column(Integer, nullable=True)  # 0-100
    
    # Relationships
    user = relationship('User', back_populates='progress')
    module = relationship('Module', back_populates='progress')
    lesson = relationship('Lesson', back_populates='progress')
    
    def __repr__(self):
        return f"<UserProgress(user_id={self.user_id}, module_id={self.module_id}, status={self.status})>"


class Interaction(Base):
    """Detailed activity log for CRA compliance reporting"""
    __tablename__ = 'interactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    interaction_type = Column(String(50), nullable=False)  # 'command', 'lesson_access', 'ai_query', 'quiz_attempt'
    command = Column(String(100), nullable=True)
    module_id = Column(Integer, nullable=True)
    lesson_id = Column(Integer, nullable=True)
    message_text = Column(Text, nullable=True)
    ai_response_length = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship('User', back_populates='interactions')
    
    def __repr__(self):
        return f"<Interaction(type={self.interaction_type}, user_id={self.user_id})>"


class PIPEDATip(Base):
    """Quick reference PIPEDA tips"""
    __tablename__ = 'pipeda_tips'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tip_code = Column(String(50), unique=True, nullable=True)
    category = Column(String(100), nullable=True)  # 'consent', 'data_breach', 'individual_rights'
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    target_audience = Column(String(100), nullable=True)  # 'citizens', 'NGOs', 'small_business'
    language = Column(String(10), default='en')
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<PIPEDATip(code={self.tip_code}, category={self.category})>"


class CRAReport(Base):
    """Pre-generated CRA impact reports"""
    __tablename__ = 'cra_reports'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    report_type = Column(String(50), nullable=False)  # 'monthly', 'quarterly', 'annual'
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    total_users = Column(Integer, default=0)
    active_users = Column(Integer, default=0)
    modules_completed = Column(Integer, default=0)
    total_interactions = Column(Integer, default=0)
    report_json = Column(Text, nullable=True)  # Full JSON data
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<CRAReport(type={self.report_type}, period={self.period_start} to {self.period_end})>"
