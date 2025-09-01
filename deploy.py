#!/usr/bin/env python3
"""
EduMorph Deployment Script
Automated deployment for development and production environments
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        sys.exit(1)

def check_requirements():
    """Check if required tools are installed"""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    # Check if virtual environment exists
    if not os.path.exists('venv'):
        print("📦 Creating virtual environment...")
        run_command('python -m venv venv', 'Virtual environment creation')
    
    print("✅ Requirements check completed")

def setup_environment():
    """Setup the development environment"""
    print("🛠️ Setting up development environment...")
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        activate_cmd = 'venv\\Scripts\\activate'
        pip_cmd = 'venv\\Scripts\\pip'
    else:  # Unix/Linux/macOS
        activate_cmd = 'source venv/bin/activate'
        pip_cmd = 'venv/bin/pip'
    
    # Install dependencies
    run_command(f'"{pip_cmd}" install --upgrade pip', 'Pip upgrade')
    run_command(f'"{pip_cmd}" install -r requirements.txt', 'Dependencies installation')
    
    # Create necessary directories
    directories = ['uploads', 'logs', 'static/images', 'static/css', 'static/js']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Copy environment file if it doesn't exist
    if not os.path.exists('.env'):
        if os.path.exists('env.example'):
            shutil.copy('env.example', '.env')
            print("📄 Created .env file from env.example")
            print("⚠️  Please update .env with your actual configuration values")
        else:
            print("⚠️  No .env file found. Please create one with your configuration")
    
    print("✅ Environment setup completed")

def setup_database():
    """Setup the database"""
    print("🗄️ Setting up database...")
    
    # Check if MySQL is available
    try:
        result = subprocess.run('mysql --version', shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠️  MySQL not found. Please install MySQL and ensure it's running")
            return
    except:
        print("⚠️  MySQL not found. Please install MySQL and ensure it's running")
        return
    
    print("📝 Database setup instructions:")
    print("1. Start MySQL service")
    print("2. Create database: CREATE DATABASE edumorph;")
    print("3. Update .env file with your database credentials")
    print("4. Run: python run.py (this will create tables automatically)")
    
    print("✅ Database setup instructions provided")

def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    
    # Check if pytest is installed
    try:
        if os.name == 'nt':  # Windows
            run_command('"venv\\Scripts\\pytest" tests/ -v', 'Test execution')
        else:  # Unix/Linux/macOS
            run_command('venv/bin/pytest tests/ -v', 'Test execution')
    except:
        print("⚠️  Tests not found or pytest not installed. Skipping tests.")
    
    print("✅ Tests completed")

def start_development():
    """Start the development server"""
    print("🚀 Starting development server...")
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = 'True'
    
    # Start the Flask application
    if os.name == 'nt':  # Windows
        run_command('"venv\\Scripts\\python" run.py', 'Development server startup')
    else:  # Unix/Linux/macOS
        run_command('venv/bin/python run.py', 'Development server startup')

def deploy_production():
    """Deploy to production"""
    print("🚀 Deploying to production...")
    
    # Check if gunicorn is installed
    try:
        if os.name == 'nt':  # Windows
            run_command('"venv\\Scripts\\pip" install gunicorn', 'Gunicorn installation')
        else:  # Unix/Linux/macOS
            run_command('venv/bin/pip install gunicorn', 'Gunicorn installation')
    except:
        print("⚠️  Failed to install gunicorn")
    
    # Set production environment
    os.environ['FLASK_ENV'] = 'production'
    
    print("📝 Production deployment instructions:")
    print("1. Update .env file with production settings")
    print("2. Set SECRET_KEY to a secure random value")
    print("3. Configure production database")
    print("4. Run: gunicorn -w 4 -b 0.0.0.0:5000 run:app")
    
    print("✅ Production deployment instructions provided")

def main():
    """Main deployment function"""
    print("🎓 EduMorph Deployment Script")
    print("Supporting SDG 4: Quality Education for All Ages")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage: python deploy.py [setup|dev|prod|test]")
        print("  setup - Setup development environment")
        print("  dev   - Start development server")
        print("  prod  - Deploy to production")
        print("  test  - Run tests")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'setup':
        check_requirements()
        setup_environment()
        setup_database()
        print("\n🎉 Setup completed! You can now run 'python deploy.py dev' to start the development server")
        
    elif command == 'dev':
        start_development()
        
    elif command == 'prod':
        deploy_production()
        
    elif command == 'test':
        run_tests()
        
    else:
        print(f"❌ Unknown command: {command}")
        print("Available commands: setup, dev, prod, test")
        sys.exit(1)

if __name__ == '__main__':
    main()
