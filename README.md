# EduMorph - AI-Powered Educational Platform

![EduMorph Logo](static/images/logo.png)

**Supporting SDG 4: Quality Education for All Ages**

EduMorph is a comprehensive AI-powered educational platform that transforms any content into interactive learning materials. Built with accessibility and inclusivity at its core, EduMorph supports learners of all ages and abilities, making quality education accessible to everyone.

## 🌟 Features

### 🤖 AI-Powered Content Processing
- **Multi-Format Input**: Upload text, PDFs, audio, video, or YouTube links
- **Smart Content Analysis**: AI automatically extracts key concepts and generates educational materials
- **Intelligent Summarization**: Creates concise summaries and key points from any content
- **Automated Question Generation**: Generates practice questions and assessments
- **Flashcard Creation**: Creates interactive flashcards for active recall

### 👥 Age-Adaptive Learning
- **Children (5-12)**: Colorful, interactive interface with simple navigation
- **Teens (13-17)**: Modern, gamified interface with social features
- **Young Adults (18-25)**: Professional interface with career-focused content
- **Adults (26+)**: Clean, efficient interface with comprehensive analytics

### ♿ Accessibility First
- **Screen Reader Support**: Full compatibility with assistive technologies
- **High Contrast Mode**: Enhanced visibility for users with visual impairments
- **Keyboard Navigation**: Complete keyboard accessibility
- **Voice Control**: Voice commands for hands-free operation
- **Font Size Adjustment**: Customizable text sizes
- **Reduced Motion**: Respects user motion preferences

### 📊 Progress Tracking & Analytics
- **Learning Streaks**: Track consecutive days of learning activity
- **Performance Analytics**: Detailed insights into learning progress
- **Subject Performance**: Track performance across different subjects
- **Personalized Recommendations**: AI-powered content suggestions
- **Engagement Metrics**: Monitor learning engagement and behavior

### 🔍 Smart Search & Discovery
- **Instant Search**: Real-time search with autocomplete
- **Voice Search**: Search using voice commands
- **Content Filtering**: Filter by subject, age group, and difficulty
- **Personalized Results**: Search results tailored to user preferences

### 📱 Multi-Platform Support
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Offline Support**: Download content for offline learning
- **Low-Bandwidth Optimized**: Efficient for users with limited internet
- **Cross-Platform Sync**: Access content across all devices

## 🏗️ Architecture

### Backend (Python/Flask)
- **Flask Application**: Modular blueprint architecture
- **SQLAlchemy ORM**: Database abstraction and management
- **MySQL Database**: Robust data storage and retrieval
- **Flask-Login**: User authentication and session management
- **RESTful API**: Comprehensive API for external integrations

### Frontend (HTML5/CSS3/JavaScript)
- **Responsive Design**: Mobile-first approach with CSS Grid and Flexbox
- **Age-Adaptive Themes**: Different visual styles for different age groups
- **Accessibility Features**: WCAG 2.1 AA compliant
- **Progressive Enhancement**: Works without JavaScript
- **Modern JavaScript**: ES6+ with accessibility considerations

### AI Integration
- **Hugging Face Transformers**: Natural language processing
- **OpenAI API**: Advanced content generation
- **Content Processing**: Multi-format file handling
- **Smart Analytics**: Learning pattern recognition

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Node.js 16+ (for development tools)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Wanchah/Testing.git
   cd Testing
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup database**
   ```bash
   mysql -u root -p
   CREATE DATABASE edumorph;
   ```

5. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

```
EduMorph/
├── app/                    # Flask application
│   ├── __init__.py        # Application factory
│   ├── auth.py            # Authentication blueprint
│   ├── main.py            # Main routes blueprint
│   ├── lessons.py         # Lessons management
│   ├── ai_services.py     # AI processing services
│   ├── dashboard.py       # User dashboards
│   └── api.py             # RESTful API endpoints
├── database/
│   └── models.py          # SQLAlchemy models
├── static/                # Static assets
│   ├── css/              # Stylesheets
│   │   ├── main.css      # Main styles
│   │   ├── themes.css    # Age-adaptive themes
│   │   └── accessibility.css # Accessibility features
│   ├── js/               # JavaScript files
│   │   ├── main.js       # Main functionality
│   │   ├── search.js     # Search features
│   │   └── accessibility.js # Accessibility features
│   └── images/           # Images and icons
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── main/             # Main pages
│   ├── auth/             # Authentication pages
│   ├── lessons/          # Lesson pages
│   └── dashboard/        # Dashboard pages
├── uploads/              # File uploads
├── requirements.txt      # Python dependencies
├── run.py               # Application entry point
└── README.md            # This file
```

## 🎯 SDG 4 Alignment

EduMorph directly supports the United Nations Sustainable Development Goal 4: Quality Education by:

### 🎓 Inclusive Education
- **Universal Access**: Free and accessible to all learners
- **Age-Inclusive**: Content adapted for all age groups (5+ years)
- **Ability-Inclusive**: Full accessibility support for learners with disabilities
- **Language Support**: Multi-language content processing

### 🌍 Global Reach
- **Low-Bandwidth Optimized**: Works in areas with limited internet
- **Offline Capabilities**: Download content for offline learning
- **Mobile-First**: Accessible on any device
- **Open Source**: Free and open for global adoption

### 📚 Quality Learning
- **AI-Enhanced Content**: Intelligent content processing and generation
- **Personalized Learning**: Adaptive content based on user needs
- **Progress Tracking**: Comprehensive learning analytics
- **Engagement Tools**: Interactive learning materials

### 🔧 Teacher Support
- **Content Creation Tools**: Easy lesson creation and management
- **Student Analytics**: Track student progress and engagement
- **Resource Sharing**: Share content with other educators
- **Assessment Tools**: Automated quiz and assessment generation

## 🛠️ Development

### Running in Development Mode
```bash
export FLASK_ENV=development
python run.py
```

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
# Format code
black app/ database/ run.py

# Lint code
flake8 app/ database/ run.py

# Type checking
mypy app/ database/ run.py
```

### Database Migrations
```bash
# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade
```

## 🚀 Deployment

### Production Deployment
1. **Set environment variables**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key
   export DATABASE_URL=mysql://user:password@host:port/database
   ```

2. **Install production dependencies**
   ```bash
   pip install gunicorn
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

### Docker Deployment
```bash
# Build image
docker build -t edumorph .

# Run container
docker run -p 5000:5000 edumorph
```

### Heroku Deployment
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main
```

## 📊 API Documentation

### Authentication Endpoints
- `POST /auth/login` - User login
- `POST /auth/signup` - User registration
- `POST /auth/logout` - User logout

### Content Endpoints
- `GET /api/v1/lessons` - List lessons
- `GET /api/v1/lessons/{id}` - Get lesson details
- `POST /ai/process-lesson` - Process new lesson content

### Search Endpoints
- `GET /search` - Search content
- `GET /search/autocomplete` - Get search suggestions

### User Endpoints
- `GET /api/v1/user/progress` - Get user progress
- `GET /api/v1/user/recommendations` - Get recommendations

## 🤝 Contributing

We welcome contributions to EduMorph! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Code of Conduct
Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **United Nations**: For the Sustainable Development Goals framework
- **Hugging Face**: For open-source AI models and tools
- **OpenAI**: For advanced AI capabilities
- **Flask Community**: For the excellent web framework
- **Accessibility Community**: For guidance on inclusive design

## 📞 Support

- **Documentation**: [docs.edumorph.org](https://docs.edumorph.org)
- **Issues**: [GitHub Issues](https://github.com/your-username/edumorph/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/edumorph/discussions)
- **Email**: support@edumorph.org

## 🌟 Roadmap

### Phase 1 (Current)
- ✅ Core platform functionality
- ✅ AI content processing
- ✅ Age-adaptive interfaces
- ✅ Accessibility features

### Phase 2 (Q2 2024)
- 🔄 Mobile app development
- 🔄 Advanced AI features
- 🔄 Multi-language support
- 🔄 Teacher collaboration tools

### Phase 3 (Q3 2024)
- 📋 Gamification features
- 📋 Social learning features
- 📋 Advanced analytics
- 📋 Integration with LMS platforms

### Phase 4 (Q4 2024)
- 📋 AR/VR learning experiences
- 📋 Advanced personalization
- 📋 Global content partnerships
- 📋 Enterprise features

---

**EduMorph - Transforming Education Through AI**

*Supporting SDG 4: Quality Education for All Ages*

[![SDG 4](https://img.shields.io/badge/SDG-4-blue)](https://sdgs.un.org/goals/goal4)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Accessibility](https://img.shields.io/badge/Accessibility-WCAG%202.1%20AA-purple.svg)](https://www.w3.org/WAI/WCAG21/quickref/)
"# Testing" 
