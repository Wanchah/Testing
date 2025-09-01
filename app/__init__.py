"""
EduMorph - AI-Powered Educational Platform
Supporting SDG 4: Quality Education

This module initializes the Flask application with all necessary configurations,
database connections, and AI service integrations.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
import os
from datetime import datetime
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

pymysql.install_as_MySQLdb()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='development'):
    """
    Application factory pattern for creating Flask app instances.
    Supports different configurations for development, testing, and production.
    """
    
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'))
    
    # Configuration
    if config_name == 'development':
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:WaNcHah_2002@localhost/edumorph')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = True
        app.config['UPLOAD_FOLDER'] = 'uploads'
        app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
        
    elif config_name == 'production':
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'production-secret-key')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['DEBUG'] = False
        app.config['UPLOAD_FOLDER'] = 'uploads'
        app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
        
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Create upload directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from .auth import auth_bp
    from .main import main_bp
    from .lessons import lessons_bp
    from .ai_services import ai_bp
    from .dashboard import dashboard_bp
    from .api import api_bp
    from .settings import settings_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(lessons_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(settings_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    print("🚀 EduMorph Application Initialized Successfully!")
    print("📚 Supporting SDG 4: Quality Education for All Ages")
    print("🤖 AI-Powered Learning Platform Ready")
    
    return app
