"""
EduMorph Database Models
Comprehensive data models for the AI-powered educational platform.

This module defines all database tables and relationships needed for:
- User management and authentication
- Lesson content and AI-generated materials
- Learning progress and engagement tracking
- External resources and content indexing
"""

from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import enum

# Enum for user roles and age groups
class UserRole(enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"
    PARENT = "parent"

class AgeGroup(enum.Enum):
    CHILDREN = "children"      # 5-12 years
    TEENS = "teens"            # 13-17 years
    YOUNG_ADULTS = "young_adults"  # 18-25 years
    ADULTS = "adults"          # 26+ years

class ContentFormat(enum.Enum):
    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"
    PDF = "pdf"
    DOCX = "docx"
    IMAGE = "image"
    YOUTUBE = "youtube"

class ActivityType(enum.Enum):
    LOGIN = "login"
    LESSON_VIEW = "lesson_view"
    FLASHCARD_REVIEW = "flashcard_review"
    QUIZ_ATTEMPT = "quiz_attempt"
    SEARCH = "search"
    DOWNLOAD = "download"

# User model with role-based access control
class User(UserMixin, db.Model):
    """User model supporting multiple roles and age groups."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.STUDENT)
    age_group = db.Column(db.Enum(AgeGroup), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    
    # Preferences for UI customization
    theme_preference = db.Column(db.String(20), default='modern')
    color_scheme = db.Column(db.String(20), default='default')
    font_size = db.Column(db.String(20), default='medium')
    font_family = db.Column(db.String(50), default='system')
    background_color = db.Column(db.String(7), default='#ffffff')
    accent_color = db.Column(db.String(7), default='#4f46e5')
    sidebar_position = db.Column(db.String(10), default='left')
    content_width = db.Column(db.String(20), default='standard')
    navigation_style = db.Column(db.String(20), default='standard')
    card_layout = db.Column(db.String(20), default='grid')
    high_contrast = db.Column(db.Boolean, default=False)
    reduced_motion = db.Column(db.Boolean, default=False)
    screen_reader_support = db.Column(db.Boolean, default=False)
    focus_indicators = db.Column(db.Boolean, default=True)
    accessibility_features = db.Column(db.JSON, default={})
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    lessons_created = db.relationship('Lesson', backref='teacher', lazy='dynamic')
    revision_logs = db.relationship('RevisionLog', backref='user', lazy='dynamic')
    engagement_metrics = db.relationship('EngagementMetric', backref='user', lazy='dynamic')
    questions_asked = db.relationship('Question', backref='student', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify user password."""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def is_teacher(self):
        """Check if user is a teacher."""
        return self.role in [UserRole.TEACHER, UserRole.ADMIN]
    
    def __repr__(self):
        return f'<User {self.username}>'

# Add these new models after the existing User model

class Document(db.Model):
    """Document model for storing uploaded files and their metadata."""
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_length = db.Column(db.Integer, default=0)
    file_type = db.Column(db.String(20), nullable=False)
    source_url = db.Column(db.String(500))  # For YouTube/online sources
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_processed = db.Column(db.Boolean, default=False)
    
    # Relationships
    user = db.relationship('User', backref='documents')
    content = db.relationship('Content', backref='document', uselist=False)
    
    def __repr__(self):
        return f'<Document {self.filename}>'

class Content(db.Model):
    """Content model for storing extracted and AI-generated content."""
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    raw_content = db.Column(db.Text, nullable=False)
    ai_generated_notes = db.Column(db.Text)
    ai_generated_summary = db.Column(db.Text)
    key_concepts = db.Column(db.Text)
    content_metadata = db.Column(db.JSON)  # Store additional metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='contents')
    
    def __repr__(self):
        return f'<Content {self.id}>'

class AIChat(db.Model):
    """AI Chat model for storing conversation history."""
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    context = db.Column(db.String(100), default='general')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='ai_chats')
    
    def __repr__(self):
        return f'<AIChat {self.id}>'

# Lesson model for storing educational content
class Lesson(db.Model):
    """Lesson model for storing various types of educational content."""
    
    __tablename__ = 'lessons'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    topic = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    
    # Content details
    raw_input = db.Column(db.Text, nullable=True)  # Original text input
    format_type = db.Column(db.Enum(ContentFormat), nullable=False)
    file_path = db.Column(db.String(500), nullable=True)  # For uploaded files
    external_url = db.Column(db.String(500), nullable=True)  # For YouTube links etc.
    
    # AI-generated content
    ai_summary = db.Column(db.Text, nullable=True)
    key_points = db.Column(db.JSON, nullable=True)  # List of key concepts
    difficulty_level = db.Column(db.String(20), default='intermediate')
    estimated_duration = db.Column(db.Integer, nullable=True)  # in minutes
    
    # Metadata
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    age_group_target = db.Column(db.Enum(AgeGroup), nullable=False)
    tags = db.Column(db.JSON, default=[])  # List of tags for search
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)
    
    # Relationships
    flashcards = db.relationship('Flashcard', backref='lesson', lazy='dynamic', cascade='all, delete-orphan')
    questions = db.relationship('Question', backref='lesson', lazy='dynamic', cascade='all, delete-orphan')
    revision_logs = db.relationship('RevisionLog', backref='lesson', lazy='dynamic')
    
    def __repr__(self):
        return f'<Lesson {self.title}>'

# Flashcard model for AI-generated study materials
class Flashcard(db.Model):
    """Flashcard model for AI-generated study materials."""
    
    __tablename__ = 'flashcards'
    
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=True)  # Can be linked to lesson or content
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=True)  # Link to AI-processed content
    
    # Flashcard content
    term = db.Column(db.String(200), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    context = db.Column(db.Text, nullable=True)  # Additional context
    example = db.Column(db.Text, nullable=True)  # Usage example
    
    # AI generation metadata
    ai_generated = db.Column(db.Boolean, default=True)
    confidence_score = db.Column(db.Float, nullable=True)  # AI confidence in generation
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Flashcard {self.term}>'

# Question model for practice and assessment
class Question(db.Model):
    """Question model for practice questions and assessments."""
    
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=True)  # Can be linked to lesson or content
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=True)  # Link to AI-processed content
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # For student questions
    
    # Question content
    question_text = db.Column(db.Text, nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), default='multiple_choice')  # multiple_choice, true_false, essay
    options = db.Column(db.JSON, nullable=True)  # For multiple choice questions
    correct_answer = db.Column(db.String(10), nullable=True)  # For multiple choice
    
    # AI generation metadata
    ai_generated = db.Column(db.Boolean, default=True)
    difficulty_level = db.Column(db.String(20), default='medium')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Question {self.question_text[:50]}...>'

# Revision log for tracking learning progress
class RevisionLog(db.Model):
    """Revision log for tracking user learning progress and performance."""
    
    __tablename__ = 'revision_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    
    # Performance metrics
    score = db.Column(db.Float, nullable=True)  # Quiz score or performance rating
    time_spent = db.Column(db.Integer, nullable=True)  # Time spent in seconds
    completion_rate = db.Column(db.Float, nullable=True)  # Percentage completed
    
    # Revision metadata
    revision_type = db.Column(db.String(50), default='review')  # review, quiz, flashcard
    notes = db.Column(db.Text, nullable=True)  # User notes during revision
    
    # Timestamps
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<RevisionLog {self.user_id} - {self.lesson_id}>'

# External resources for content integration
class ExternalResource(db.Model):
    """External resource model for integrating content from other platforms."""
    
    __tablename__ = 'external_resources'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Resource details
    title = db.Column(db.String(200), nullable=False)
    source_url = db.Column(db.String(500), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    format_type = db.Column(db.Enum(ContentFormat), nullable=False)
    
    # Content processing
    raw_content = db.Column(db.Text, nullable=True)  # Extracted content
    processed_content = db.Column(db.JSON, nullable=True)  # AI-processed content
    ai_summary = db.Column(db.Text, nullable=True)
    
    # Metadata
    age_group_target = db.Column(db.Enum(AgeGroup), nullable=False)
    difficulty_level = db.Column(db.String(20), default='intermediate')
    tags = db.Column(db.JSON, default=[])
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<ExternalResource {self.title}>'

# Engagement metrics for analytics
class EngagementMetric(db.Model):
    """Engagement metrics for tracking user activity and behavior."""
    
    __tablename__ = 'engagement_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Activity details
    activity_type = db.Column(db.Enum(ActivityType), nullable=False)
    activity_data = db.Column(db.JSON, nullable=True)  # Additional activity data
    session_duration = db.Column(db.Integer, nullable=True)  # Session duration in seconds
    
    # Timestamps
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EngagementMetric {self.user_id} - {self.activity_type}>'

# User session management
class UserSession(db.Model):
    """User session model for managing active sessions and preferences."""
    
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_token = db.Column(db.String(255), unique=True, nullable=False)
    
    # Session data
    current_lesson = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=True)
    progress_data = db.Column(db.JSON, nullable=True)  # Current progress state
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<UserSession {self.user_id}>'

# Content search index for fast retrieval
class SearchIndex(db.Model):
    """Search index for fast content retrieval and search functionality."""
    
    __tablename__ = 'search_index'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Indexed content
    content_type = db.Column(db.String(50), nullable=False)  # lesson, flashcard, question, resource
    content_id = db.Column(db.Integer, nullable=False)  # ID of the indexed content
    searchable_text = db.Column(db.Text, nullable=False)  # Text content for search
    
    # Search metadata
    keywords = db.Column(db.JSON, default=[])  # Extracted keywords
    topic_tags = db.Column(db.JSON, default=[])  # Topic tags
    subject_tags = db.Column(db.JSON, default=[])  # Subject tags
    
    # Timestamps
    indexed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SearchIndex {self.content_type}:{self.content_id}>'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login."""
    return User.query.get(int(user_id))
