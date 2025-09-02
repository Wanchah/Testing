"""
EduMorph Main Blueprint
Core application routes and functionality for the main application.

This module handles:
- Home page and landing
- Search functionality
- Basic navigation
- Age-adaptive content delivery
"""

from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from database.models import Lesson, Flashcard, Question, ExternalResource, SearchIndex
from sqlalchemy import or_
from app import db
import json

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    Main landing page with age-adaptive content and features showcase.
    Supports SDG 4: Quality Education for all age groups.
    """
    
    # Get user's age group for personalized content
    age_group = None
    if current_user.is_authenticated:
        age_group = current_user.age_group.value
    
    # Get featured lessons for different age groups
    featured_lessons = {
        'children': Lesson.query.filter_by(age_group_target='children', is_published=True).limit(6).all(),
        'teens': Lesson.query.filter_by(age_group_target='teens', is_published=True).limit(6).all(),
        'young_adults': Lesson.query.filter_by(age_group_target='young_adults', is_published=True).limit(6).all(),
        'adults': Lesson.query.filter_by(age_group_target='adults', is_published=True).limit(6).all()
    }
    
    return render_template('main/index.html', 
                         featured_lessons=featured_lessons,
                         user_age_group=age_group)

@main_bp.route('/search')
def search():
    """
    Smart search functionality with results page.
    Searches across all content types: lessons, flashcards, questions, resources.
    """
    
    query = request.args.get('q', '').strip()
    content_type = request.args.get('type', 'all')
    age_group = request.args.get('age_group', 'all')
    subject = request.args.get('subject', 'all')
    
    if not query:
        return render_template('main/search.html', results=[], query='', total=0)
    
    # For now, return sample results since SearchIndex model might not exist
    # In a real implementation, you would query the database
    sample_results = [
        {
            'type': 'lesson',
            'id': 1,
            'title': 'Introduction to Algebra',
            'description': 'Learn the fundamentals of algebraic expressions and equations through interactive examples.',
            'topic': 'Algebra',
            'subject': 'mathematics',
            'age_group': 'teens',
            'url': '/lessons/1'
        },
        {
            'type': 'flashcard',
            'id': 1,
            'term': 'Variable',
            'definition': 'A symbol (usually a letter) that represents a number that can change.',
            'lesson_id': 1,
            'url': '/flashcards/1'
        },
        {
            'type': 'question',
            'id': 1,
            'question': 'What is the value of x in the equation 2x + 5 = 13?',
            'lesson_id': 1,
            'url': '/questions/1'
        }
    ]
    
    # Filter results based on parameters
    filtered_results = []
    for result in sample_results:
        if content_type != 'all' and result['type'] != content_type:
            continue
        if subject != 'all' and result.get('subject') != subject:
            continue
        if age_group != 'all' and result.get('age_group') != age_group:
            continue
        filtered_results.append(result)
    
    return render_template('main/search.html', 
                         results=filtered_results, 
                         query=query, 
                         total=len(filtered_results))

# Convenience redirects for the AI web search feature
@main_bp.route('/web-search')
@main_bp.route('/google-search')
def redirect_web_search():
    from flask import redirect, url_for
    return redirect(url_for('ai_services.web_search'))

@main_bp.route('/about')
def about():
    """About page with information about EduMorph and SDG 4."""
    return render_template('main/about.html')

@main_bp.route('/contact')
def contact():
    """Contact page with contact information and support."""
    return render_template('main/contact.html')

@main_bp.route('/search/autocomplete')
def search_autocomplete():
    """
    Autocomplete endpoint for search suggestions.
    Provides instant search suggestions as user types.
    """
    
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify({'suggestions': []})
    
    # Get suggestions from search index
    suggestions = SearchIndex.query.filter(
        SearchIndex.searchable_text.contains(query)
    ).limit(10).all()
    
    # Extract unique suggestions
    unique_suggestions = []
    seen = set()
    
    for suggestion in suggestions:
        # Extract relevant text snippets
        text = suggestion.searchable_text
        words = text.split()
        
        for word in words:
            if query.lower() in word.lower() and word.lower() not in seen:
                seen.add(word.lower())
                unique_suggestions.append(word)
                
                if len(unique_suggestions) >= 10:
                    break
        
        if len(unique_suggestions) >= 10:
            break
    
    return jsonify({'suggestions': unique_suggestions[:10]})

@main_bp.route('/browse')
def browse():
    """
    Browse page for exploring content by category, subject, and age group.
    Provides organized content discovery for different user types.
    """
    
    # Get filter parameters
    subject = request.args.get('subject', 'all')
    age_group = request.args.get('age_group', 'all')
    difficulty = request.args.get('difficulty', 'all')
    
    # Build query
    query = Lesson.query.filter_by(is_published=True)
    
    if subject != 'all':
        query = query.filter(Lesson.subject == subject)
    
    if age_group != 'all':
        query = query.filter(Lesson.age_group_target == age_group)
    
    if difficulty != 'all':
        query = query.filter(Lesson.difficulty_level == difficulty)
    
    # Get lessons
    lessons = query.order_by(Lesson.created_at.desc()).limit(50).all()
    
    # Get available subjects and age groups for filters
    subjects = db.session.query(Lesson.subject).distinct().all()
    age_groups = db.session.query(Lesson.age_group_target).distinct().all()
    difficulty_levels = db.session.query(Lesson.difficulty_level).distinct().all()
    
    return render_template('main/browse.html',
                         lessons=lessons,
                         subjects=[s[0] for s in subjects],
                         age_groups=[ag[0].value for ag in age_groups],
                         difficulty_levels=[dl[0] for dl in difficulty_levels],
                         current_filters={
                             'subject': subject,
                             'age_group': age_group,
                             'difficulty': difficulty
                         })



@main_bp.route('/accessibility')
def accessibility():
    """
    Accessibility features and settings page.
    Supports inclusive education for all learners.
    """
    
    return render_template('main/accessibility.html')

@main_bp.route('/api/stats')
def api_stats():
    """
    API endpoint for platform statistics.
    Used for dashboard and analytics.
    """
    
    try:
        stats = {
            'total_lessons': Lesson.query.count(),
            'total_flashcards': Flashcard.query.count(),
            'total_questions': Question.query.count(),
            'total_resources': ExternalResource.query.count(),
            'published_lessons': Lesson.query.filter_by(is_published=True).count(),
            'ai_generated_content': Flashcard.query.filter_by(ai_generated=True).count() + 
                                   Question.query.filter_by(ai_generated=True).count()
        }
        
        return jsonify({'success': True, 'stats': stats})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@main_bp.route('/api/age-group-content/<age_group>')
def api_age_group_content(age_group):
    """
    API endpoint for age-specific content recommendations.
    Supports personalized learning for different age groups.
    """
    
    try:
        # Validate age group
        valid_age_groups = ['children', 'teens', 'young_adults', 'adults']
        if age_group not in valid_age_groups:
            return jsonify({'error': 'Invalid age group'}), 400
        
        # Get content for specific age group
        lessons = Lesson.query.filter_by(
            age_group_target=age_group,
            is_published=True
        ).order_by(Lesson.created_at.desc()).limit(10).all()
        
        content = []
        for lesson in lessons:
            content.append({
                'id': lesson.id,
                'title': lesson.title,
                'topic': lesson.topic,
                'subject': lesson.subject,
                'difficulty': lesson.difficulty_level,
                'duration': lesson.estimated_duration,
                'url': f'/lessons/{lesson.id}'
            })
        
        return jsonify({
            'success': True,
            'age_group': age_group,
            'content': content,
            'total': len(content)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
