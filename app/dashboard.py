"""
EduMorph Dashboard Blueprint
Role-based dashboards for different user types with analytics and progress tracking.

This module handles:
- Student dashboard with learning progress and recommendations
- Teacher dashboard with lesson management and analytics
- Parent dashboard with child progress monitoring
- Admin dashboard with platform analytics and management
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from database.models import User, Lesson, Flashcard, Question, RevisionLog, EngagementMetric, UserRole
from app import db
from sqlalchemy import func
from datetime import datetime, timedelta
import json

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def dashboard_index():
    """Redirect user to role-appropriate dashboard."""
    if current_user.role == UserRole.STUDENT:
        return redirect(url_for('dashboard.student_dashboard'))
    if current_user.role == UserRole.TEACHER or current_user.role == UserRole.ADMIN:
        return redirect(url_for('dashboard.teacher_dashboard'))
    if current_user.role == UserRole.PARENT:
        return redirect(url_for('dashboard.parent_dashboard'))
    return redirect(url_for('main.index'))

@dashboard_bp.route('/student')
@login_required
def student_dashboard():
    """
    Student dashboard with personalized learning progress and recommendations.
    Age-adaptive interface based on student's age group.
    """
    
    if current_user.role.value != 'student':
        flash('Access denied. This dashboard is for students only.', 'error')
        return redirect(url_for('main.index'))
    
    # Get student's learning progress
    recent_lessons = RevisionLog.query.filter_by(user_id=current_user.id)\
        .order_by(RevisionLog.timestamp.desc()).limit(5).all()
    
    # Get recommended lessons based on age group
    recommended_lessons = Lesson.query.filter_by(
        age_group_target=current_user.age_group,
        is_published=True
    ).order_by(Lesson.created_at.desc()).limit(6).all()
    
    # Calculate learning statistics
    total_lessons_completed = RevisionLog.query.filter_by(user_id=current_user.id).count()
    total_flashcards_reviewed = EngagementMetric.query.filter_by(
        user_id=current_user.id,
        activity_type='flashcard_review'
    ).count()
    
    # Get current streak (consecutive days with activity)
    streak = calculate_learning_streak(current_user.id)
    
    # Get performance by subject
    subject_performance = get_subject_performance(current_user.id)
    
    return render_template('dashboard/student.html',
                         recent_lessons=recent_lessons,
                         recommended_lessons=recommended_lessons,
                         total_lessons_completed=total_lessons_completed,
                         total_flashcards_reviewed=total_flashcards_reviewed,
                         streak=streak,
                         subject_performance=subject_performance,
                         user_age_group=current_user.age_group.value)

@dashboard_bp.route('/teacher')
@login_required
def teacher_dashboard():
    """
    Teacher dashboard with lesson management and student analytics.
    """
    
    if not current_user.is_teacher():
        flash('Access denied. This dashboard is for teachers only.', 'error')
        return redirect(url_for('main.index'))
    
    # Get teacher's lessons
    teacher_lessons = Lesson.query.filter_by(teacher_id=current_user.id)\
        .order_by(Lesson.created_at.desc()).limit(10).all()
    
    # Get lesson statistics
    total_lessons = Lesson.query.filter_by(teacher_id=current_user.id).count()
    published_lessons = Lesson.query.filter_by(
        teacher_id=current_user.id,
        is_published=True
    ).count()
    
    # Get total flashcards and questions created
    total_flashcards = 0
    total_questions = 0
    for lesson in teacher_lessons:
        total_flashcards += lesson.flashcards.count()
        total_questions += lesson.questions.count()
    
    # Get student engagement metrics for teacher's lessons
    lesson_engagement = get_lesson_engagement_stats(current_user.id)
    
    return render_template('dashboard/teacher.html',
                         teacher_lessons=teacher_lessons,
                         total_lessons=total_lessons,
                         published_lessons=published_lessons,
                         total_flashcards=total_flashcards,
                         total_questions=total_questions,
                         lesson_engagement=lesson_engagement)

@dashboard_bp.route('/parent')
@login_required
def parent_dashboard():
    """
    Parent dashboard for monitoring child's learning progress.
    """
    
    if current_user.role.value != 'parent':
        flash('Access denied. This dashboard is for parents only.', 'error')
        return redirect(url_for('main.index'))
    
    # Get children (students) associated with this parent
    # For now, we'll show a placeholder - in production, implement parent-child relationships
    children = []  # Placeholder for child accounts
    
    # Get overall platform statistics for children
    child_stats = {
        'total_lessons_completed': 0,
        'total_time_spent': 0,
        'average_scores': 0,
        'current_streak': 0
    }
    
    return render_template('dashboard/parent.html',
                         children=children,
                         child_stats=child_stats)

@dashboard_bp.route('/admin')
@login_required
def admin_dashboard():
    """
    Admin dashboard with platform-wide analytics and management tools.
    """
    
    if current_user.role.value != 'admin':
        flash('Access denied. This dashboard is for administrators only.', 'error')
        return redirect(url_for('main.index'))
    
    # Get platform statistics
    total_users = User.query.count()
    total_lessons = Lesson.query.count()
    total_flashcards = Flashcard.query.count()
    total_questions = Question.query.count()
    
    # Get user statistics by role
    user_stats = {
        'students': User.query.filter_by(role='student').count(),
        'teachers': User.query.filter_by(role='teacher').count(),
        'parents': User.query.filter_by(role='parent').count(),
        'admins': User.query.filter_by(role='admin').count()
    }
    
    # Get recent activity
    recent_activity = EngagementMetric.query\
        .order_by(EngagementMetric.timestamp.desc()).limit(20).all()
    
    # Get lesson statistics by age group
    age_group_stats = get_age_group_lesson_stats()
    
    return render_template('dashboard/admin.html',
                         total_users=total_users,
                         total_lessons=total_lessons,
                         total_flashcards=total_flashcards,
                         total_questions=total_questions,
                         user_stats=user_stats,
                         recent_activity=recent_activity,
                         age_group_stats=age_group_stats)

@dashboard_bp.route('/api/progress-chart')
@login_required
def api_progress_chart():
    """
    API endpoint for learning progress chart data.
    """
    
    try:
        # Get last 30 days of activity
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        # Get daily activity counts
        daily_activity = db.session.query(
            func.date(EngagementMetric.timestamp).label('date'),
            func.count(EngagementMetric.id).label('count')
        ).filter(
            EngagementMetric.user_id == current_user.id,
            EngagementMetric.timestamp >= start_date,
            EngagementMetric.timestamp <= end_date
        ).group_by(func.date(EngagementMetric.timestamp)).all()
        
        # Format data for chart
        chart_data = []
        for activity in daily_activity:
            chart_data.append({
                'date': activity.date.isoformat(),
                'count': activity.count
            })
        
        return jsonify({
            'success': True,
            'data': chart_data
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@dashboard_bp.route('/api/performance-summary')
@login_required
def api_performance_summary():
    """
    API endpoint for user performance summary.
    """
    
    try:
        # Get user's revision logs
        revision_logs = RevisionLog.query.filter_by(user_id=current_user.id).all()
        
        if not revision_logs:
            return jsonify({
                'success': True,
                'summary': {
                    'total_attempts': 0,
                    'average_score': 0,
                    'best_score': 0,
                    'improvement_trend': 'stable'
                }
            })
        
        # Calculate performance metrics
        total_attempts = len(revision_logs)
        scores = [log.score for log in revision_logs if log.score is not None]
        
        if scores:
            average_score = sum(scores) / len(scores)
            best_score = max(scores)
            
            # Calculate improvement trend
            if len(scores) >= 5:
                recent_scores = scores[-5:]
                older_scores = scores[:5] if len(scores) >= 10 else scores[:len(scores)//2]
                recent_avg = sum(recent_scores) / len(recent_scores)
                older_avg = sum(older_scores) / len(older_scores)
                
                if recent_avg > older_avg + 5:
                    trend = 'improving'
                elif recent_avg < older_avg - 5:
                    trend = 'declining'
                else:
                    trend = 'stable'
            else:
                trend = 'stable'
        else:
            average_score = 0
            best_score = 0
            trend = 'stable'
        
        return jsonify({
            'success': True,
            'summary': {
                'total_attempts': total_attempts,
                'average_score': round(average_score, 1),
                'best_score': round(best_score, 1),
                'improvement_trend': trend
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def calculate_learning_streak(user_id):
    """
    Calculate consecutive days of learning activity.
    """
    
    try:
        # Get all activity dates for the user
        activity_dates = db.session.query(
            db.func.date(EngagementMetric.timestamp).label('date')
        ).filter_by(user_id=user_id).distinct().order_by('date').all()
        
        if not activity_dates:
            return 0
        
        # Convert to date objects
        dates = [activity.date for activity in activity_dates]
        
        # Calculate streak
        streak = 0
        current_date = datetime.utcnow().date()
        
        for i in range(len(dates) - 1, -1, -1):
            if dates[i] == current_date - timedelta(days=streak):
                streak += 1
            else:
                break
        
        return streak
        
    except Exception as e:
        print(f"Error calculating learning streak: {e}")
        return 0

def get_subject_performance(user_id):
    """
    Get performance statistics by subject.
    """
    
    try:
        # Get revision logs with lesson information
        performance_data = db.session.query(
            Lesson.subject,
            func.avg(RevisionLog.score).label('avg_score'),
            func.count(RevisionLog.id).label('attempts')
        ).join(RevisionLog, Lesson.id == RevisionLog.lesson_id)\
        .filter(RevisionLog.user_id == user_id)\
        .group_by(Lesson.subject).all()
        
        subject_performance = []
        for data in performance_data:
            subject_performance.append({
                'subject': data.subject,
                'average_score': round(data.avg_score, 1) if data.avg_score else 0,
                'attempts': data.attempts
            })
        
        return subject_performance
        
    except Exception as e:
        print(f"Error getting subject performance: {e}")
        return []

def get_lesson_engagement_stats(teacher_id):
    """
    Get engagement statistics for teacher's lessons.
    """
    
    try:
        # Get lessons created by teacher
        teacher_lessons = Lesson.query.filter_by(teacher_id=teacher_id).all()
        
        engagement_stats = []
        for lesson in teacher_lessons:
            # Get total views
            total_views = EngagementMetric.query.filter_by(
                activity_type='lesson_view',
                activity_data={'lesson_id': lesson.id}
            ).count()
            
            # Get total flashcards reviewed
            flashcard_reviews = EngagementMetric.query.filter_by(
                activity_type='flashcard_review',
                activity_data={'lesson_id': lesson.id}
            ).count()
            
            # Get total quiz attempts
            quiz_attempts = EngagementMetric.query.filter_by(
                activity_type='quiz_attempt',
                activity_data={'lesson_id': lesson.id}
            ).count()
            
            engagement_stats.append({
                'lesson_id': lesson.id,
                'lesson_title': lesson.title,
                'total_views': total_views,
                'flashcard_reviews': flashcard_reviews,
                'quiz_attempts': quiz_attempts
            })
        
        return engagement_stats
        
    except Exception as e:
        print(f"Error getting lesson engagement stats: {e}")
        return []

def get_age_group_lesson_stats():
    """
    Get lesson statistics by age group for admin dashboard.
    """
    
    try:
        age_group_stats = db.session.query(
            Lesson.age_group_target,
            func.count(Lesson.id).label('lesson_count'),
            func.count(Flashcard.id).label('flashcard_count'),
            func.count(Question.id).label('question_count')
        ).outerjoin(Flashcard, Lesson.id == Flashcard.lesson_id)\
        .outerjoin(Question, Lesson.id == Question.lesson_id)\
        .group_by(Lesson.age_group_target).all()
        
        stats = []
        for data in age_group_stats:
            stats.append({
                'age_group': data.age_group_target.value,
                'lesson_count': data.lesson_count,
                'flashcard_count': data.flashcard_count,
                'question_count': data.question_count
            })
        
        return stats
        
    except Exception as e:
        print(f"Error getting age group lesson stats: {e}")
        return []
