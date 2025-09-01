"""
EduMorph - Main Application Entry Point
AI-Powered Educational Platform Supporting SDG 4: Quality Education

This script initializes and runs the EduMorph Flask application.
"""

import os
from app import create_app

# Create the Flask application instance
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    print("🚀 Starting EduMorph - AI-Powered Educational Platform")
    print("📚 Supporting SDG 4: Quality Education for All Ages")
    print("🌐 Application will be available at: http://localhost:5000")
    print("🤖 AI Services: Hugging Face & OpenAI Integration")
    print("👥 Multi-Role Support: Students, Teachers, Parents, Admins")
    print("🎨 Age-Adaptive Interface: Children, Teens, Young Adults, Adults")
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
