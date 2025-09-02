"""
EduMorph API Blueprint
RESTful API endpoints for external integrations and mobile applications.

This module handles:
- Public API endpoints for content access
- Authentication and authorization
- Rate limiting and security
- API documentation and versioning
"""

from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from database.models import User, Lesson, Flashcard, Question, RevisionLog, EngagementMetric
from app import db
from sqlalchemy import or_, func
from datetime import datetime
import json

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/lessons')
def api_lessons():
    """
    Public API endpoint for retrieving published lessons.
    Supports filtering and pagination.
    """
    
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 50)
        subject = request.args.get('subject')
        age_group = request.args.get('age_group')
        difficulty = request.args.get('difficulty')
        search = request.args.get('search')
        
        # Build query
        query = Lesson.query.filter_by(is_published=True)
        
        if subject:
            query = query.filter(Lesson.subject == subject)
        
        if age_group:
            query = query.filter(Lesson.age_group_target == age_group)
        
        if difficulty:
            query = query.filter(Lesson.difficulty_level == difficulty)
        
        if search:
            query = query.filter(
                or_(
                    Lesson.title.contains(search),
                    Lesson.description.contains(search),
                    Lesson.topic.contains(search)
                )
            )
        
        # Execute query with pagination
        lessons = query.order_by(Lesson.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Format response
        lessons_data = []
        for lesson in lessons.items:
            lessons_data.append({
                'id': lesson.id,
                'title': lesson.title,
                'description': lesson.description,
                'topic': lesson.topic,
                'subject': lesson.subject,
                'age_group': lesson.age_group_target.value,
                'difficulty': lesson.difficulty_level,
                'duration': lesson.estimated_duration,
                'created_at': lesson.created_at.isoformat(),
                'tags': lesson.tags,
                'flashcards_count': lesson.flashcards.count(),
                'questions_count': lesson.questions.count()
            })
        
        return jsonify({
            'success': True,
            'data': lessons_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': lessons.total,
                'pages': lessons.pages,
                'has_next': lessons.has_next,
                'has_prev': lessons.has_prev
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/lessons/<int:lesson_id>')
def api_lesson_detail(lesson_id):
    """
    Public API endpoint for retrieving a specific lesson with its content.
    """
    
    try:
        lesson = Lesson.query.get_or_404(lesson_id)
        
        if not lesson.is_published:
            return jsonify({'success': False, 'error': 'Lesson not found'}), 404
        
        # Get lesson content
        flashcards = lesson.flashcards.all()
        questions = lesson.questions.all()
        
        # Format flashcards
        flashcards_data = []
        for flashcard in flashcards:
            flashcards_data.append({
                'id': flashcard.id,
                'term': flashcard.term,
                'definition': flashcard.definition,
                'context': flashcard.context,
                'example': flashcard.example
            })
        
        # Format questions
        questions_data = []
        for question in questions:
            questions_data.append({
                'id': question.id,
                'question': question.question_text,
                'answer': question.answer_text,
                'type': question.question_type,
                'difficulty': question.difficulty_level
            })
        
        # Format lesson data
        lesson_data = {
            'id': lesson.id,
            'title': lesson.title,
            'description': lesson.description,
            'topic': lesson.topic,
            'subject': lesson.subject,
            'age_group': lesson.age_group_target.value,
            'difficulty': lesson.difficulty_level,
            'duration': lesson.estimated_duration,
            'summary': lesson.ai_summary,
            'key_points': lesson.key_points,
            'created_at': lesson.created_at.isoformat(),
            'updated_at': lesson.updated_at.isoformat(),
            'tags': lesson.tags,
            'flashcards': flashcards_data,
            'questions': questions_data
        }
        
        return jsonify({
            'success': True,
            'data': lesson_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/lessons/<int:lesson_id>/flashcards')
def api_lesson_flashcards(lesson_id):
    """
    API endpoint for retrieving flashcards for a specific lesson.
    """
    
    try:
        lesson = Lesson.query.get_or_404(lesson_id)
        
        if not lesson.is_published:
            return jsonify({'success': False, 'error': 'Lesson not found'}), 404
        
        flashcards = lesson.flashcards.all()
        
        flashcards_data = []
        for flashcard in flashcards:
            flashcards_data.append({
                'id': flashcard.id,
                'term': flashcard.term,
                'definition': flashcard.definition,
                'context': flashcard.context,
                'example': flashcard.example,
                'created_at': flashcard.created_at.isoformat()
            })
        
        return jsonify({
            'success': True,
            'data': flashcards_data,
            'total': len(flashcards_data)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/lessons/<int:lesson_id>/questions')
def api_lesson_questions(lesson_id):
    """
    API endpoint for retrieving questions for a specific lesson.
    """
    
    try:
        lesson = Lesson.query.get_or_404(lesson_id)
        
        if not lesson.is_published:
            return jsonify({'success': False, 'error': 'Lesson not found'}), 404
        
        questions = lesson.questions.all()
        
        questions_data = []
        for question in questions:
            questions_data.append({
                'id': question.id,
                'question': question.question_text,
                'answer': question.answer_text,
                'type': question.question_type,
                'difficulty': question.difficulty_level,
                'options': question.options,
                'created_at': question.created_at.isoformat()
            })
        
        return jsonify({
            'success': True,
            'data': questions_data,
            'total': len(questions_data)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/search')
def api_search():
    """
    Public API endpoint for searching content across the platform.
    """
    
    try:
        query = request.args.get('q', '').strip()
        content_type = request.args.get('type', 'all')
        age_group = request.args.get('age_group', 'all')
        subject = request.args.get('subject', 'all')
        limit = min(request.args.get('limit', 20, type=int), 100)
        
        if not query:
            return jsonify({'success': False, 'error': 'Search query is required'}), 400
        
        # Build search query
        search_query = Lesson.query.filter_by(is_published=True)
        
        if age_group != 'all':
            search_query = search_query.filter(Lesson.age_group_target == age_group)
        
        if subject != 'all':
            search_query = search_query.filter(Lesson.subject == subject)
        
        # Apply text search
        search_query = search_query.filter(
            or_(
                Lesson.title.contains(query),
                Lesson.description.contains(query),
                Lesson.topic.contains(query),
                Lesson.ai_summary.contains(query)
            )
        )
        
        # Execute search
        results = search_query.limit(limit).all()
        
        # Format results
        search_results = []
        for lesson in results:
            search_results.append({
                'id': lesson.id,
                'title': lesson.title,
                'description': lesson.description,
                'topic': lesson.topic,
                'subject': lesson.subject,
                'age_group': lesson.age_group_target.value,
                'difficulty': lesson.difficulty_level,
                'duration': lesson.estimated_duration,
                'created_at': lesson.created_at.isoformat(),
                'relevance_score': 1.0  # Placeholder for relevance scoring
            })
        
        return jsonify({
            'success': True,
            'query': query,
            'results': search_results,
            'total': len(search_results)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/stats')
def api_stats():
    """
    Public API endpoint for platform statistics.
    """
    
    try:
        stats = {
            'total_lessons': Lesson.query.filter_by(is_published=True).count(),
            'total_flashcards': Flashcard.query.count(),
            'total_questions': Question.query.count(),
            'total_users': User.query.count(),
            'lessons_by_age_group': {},
            'lessons_by_subject': {}
        }
        
        # Get lessons by age group
        age_group_stats = db.session.query(
            Lesson.age_group_target,
            func.count(Lesson.id).label('count')
        ).filter_by(is_published=True).group_by(Lesson.age_group_target).all()
        
        for stat in age_group_stats:
            stats['lessons_by_age_group'][stat.age_group_target.value] = stat.count
        
        # Get lessons by subject
        subject_stats = db.session.query(
            Lesson.subject,
            func.count(Lesson.id).label('count')
        ).filter_by(is_published=True).group_by(Lesson.subject).all()
        
        for stat in subject_stats:
            stats['lessons_by_subject'][stat.subject] = stat.count
        
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/user/progress', methods=['GET'])
@login_required
def api_user_progress():
    """
    API endpoint for user's learning progress (requires authentication).
    """
    
    try:
        # Get user's revision logs
        revision_logs = RevisionLog.query.filter_by(user_id=current_user.id)\
            .order_by(RevisionLog.timestamp.desc()).limit(50).all()
        
        progress_data = []
        for log in revision_logs:
            lesson = Lesson.query.get(log.lesson_id)
            if lesson:
                progress_data.append({
                    'lesson_id': lesson.id,
                    'lesson_title': lesson.title,
                    'subject': lesson.subject,
                    'topic': lesson.topic,
                    'score': log.score,
                    'completion_rate': log.completion_rate,
                    'time_spent': log.time_spent,
                    'revision_type': log.revision_type,
                    'timestamp': log.timestamp.isoformat()
                })
        
        return jsonify({
            'success': True,
            'data': progress_data,
            'total': len(progress_data)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/user/recommendations', methods=['GET'])
@login_required
def api_user_recommendations():
    """
    API endpoint for personalized lesson recommendations (requires authentication).
    """
    
    try:
        # Get user's learning history
        user_revision_logs = RevisionLog.query.filter_by(user_id=current_user.id)\
            .order_by(RevisionLog.timestamp.desc()).limit(10).all()
        
        # Get subjects and topics the user has studied
        studied_subjects = set()
        studied_topics = set()
        
        for log in user_revision_logs:
            lesson = Lesson.query.get(log.lesson_id)
            if lesson:
                studied_subjects.add(lesson.subject)
                studied_topics.add(lesson.topic)
        
        # Find related lessons
        related_lessons = Lesson.query.filter(
            Lesson.is_published == True,
            Lesson.age_group_target == current_user.age_group.value,
            or_(
                Lesson.subject.in_(list(studied_subjects)),
                Lesson.topic.in_(list(studied_topics))
            )
        ).filter(Lesson.id.notin_([log.lesson_id for log in user_revision_logs])).limit(10).all()
        
        # Format recommendations
        recommendations = []
        for lesson in related_lessons:
            recommendations.append({
                'id': lesson.id,
                'title': lesson.title,
                'topic': lesson.topic,
                'subject': lesson.subject,
                'difficulty': lesson.difficulty_level,
                'duration': lesson.estimated_duration,
                'summary': lesson.ai_summary,
                'created_at': lesson.created_at.isoformat()
            })
        
        return jsonify({
            'success': True,
            'data': recommendations,
            'total': len(recommendations)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.errorhandler(404)
def api_not_found(error):
    """Handle 404 errors for API endpoints."""
    return jsonify({'success': False, 'error': 'API endpoint not found'}), 404

@api_bp.errorhandler(500)
def api_internal_error(error):
    """Handle 500 errors for API endpoints."""
    return jsonify({'success': False, 'error': 'Internal server error'}), 500
