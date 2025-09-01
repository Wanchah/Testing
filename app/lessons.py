"""
EduMorph Lessons Blueprint
Lesson management, viewing, and interaction functionality.

This module handles:
- Lesson creation and editing
- Lesson viewing with age-adaptive interface
- Flashcard and question interaction
- Progress tracking and revision
- Content organization and search
"""

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from database.models import Lesson, Flashcard, Question, RevisionLog, EngagementMetric, db, User, UserRole, AgeGroup
from datetime import datetime
import json

lessons_bp = Blueprint('lessons', __name__, url_prefix='/lessons')

def create_sample_lessons():
    """Create sample lessons if none exist in the database."""
    if Lesson.query.count() > 0:
        return  # Already have lessons
    
    # Create a sample teacher user if none exists
    teacher = User.query.filter_by(role=UserRole.TEACHER).first()
    if not teacher:
        teacher = User(
            username='sample_teacher',
            email='teacher@edumorph.com',
            first_name='Sample',
            last_name='Teacher',
            role=UserRole.TEACHER,
            age_group=AgeGroup.ADULTS
        )
        teacher.set_password('password123')
        db.session.add(teacher)
        db.session.flush()
    
    # Sample lessons data
    sample_lessons = [
        {
            'title': 'Introduction to Algebra',
            'description': 'Learn the fundamentals of algebraic expressions and equations through interactive examples.',
            'topic': 'Algebra',
            'subject': 'mathematics',
            'age_group_target': AgeGroup.TEENS,
            'difficulty_level': 'beginner',
            'content': 'Algebra is a branch of mathematics that deals with symbols and the rules for manipulating these symbols.',
            'tags': ['algebra', 'mathematics', 'equations', 'variables']
        },
        {
            'title': 'Basic Chemistry Concepts',
            'description': 'Explore the building blocks of matter and chemical reactions.',
            'topic': 'Chemistry',
            'subject': 'science',
            'age_group_target': AgeGroup.TEENS,
            'difficulty_level': 'beginner',
            'content': 'Chemistry is the study of matter and the changes it undergoes.',
            'tags': ['chemistry', 'science', 'matter', 'reactions']
        },
        {
            'title': 'World History: Ancient Civilizations',
            'description': 'Discover the fascinating world of ancient Egypt, Greece, and Rome.',
            'topic': 'Ancient History',
            'subject': 'history',
            'age_group_target': AgeGroup.TEENS,
            'difficulty_level': 'beginner',
            'content': 'Ancient civilizations laid the foundation for modern society.',
            'tags': ['history', 'ancient', 'civilizations', 'egypt', 'greece', 'rome']
        },
        {
            'title': 'Creative Writing Basics',
            'description': 'Develop your storytelling skills and creative expression.',
            'topic': 'Creative Writing',
            'subject': 'literature',
            'age_group_target': AgeGroup.TEENS,
            'difficulty_level': 'beginner',
            'content': 'Creative writing allows you to express your imagination through words.',
            'tags': ['writing', 'creative', 'literature', 'storytelling']
        }
    ]
    
    for lesson_data in sample_lessons:
        lesson = Lesson(
            title=lesson_data['title'],
            description=lesson_data['description'],
            topic=lesson_data['topic'],
            subject=lesson_data['subject'],
            age_group_target=lesson_data['age_group_target'],
            difficulty_level=lesson_data['difficulty_level'],
            content=lesson_data['content'],
            tags=lesson_data['tags'],
            teacher_id=teacher.id,
            is_published=True
        )
        db.session.add(lesson)
        db.session.flush()
        
        # Create sample flashcards for each lesson
        if lesson.subject == 'mathematics':
            sample_flashcards = [
                {'term': 'Variable', 'definition': 'A symbol (usually a letter) that represents a number that can change.'},
                {'term': 'Equation', 'definition': 'A mathematical statement that shows two expressions are equal.'},
                {'term': 'Expression', 'definition': 'A combination of numbers, variables, and operations.'}
            ]
        elif lesson.subject == 'science':
            sample_flashcards = [
                {'term': 'Atom', 'definition': 'The smallest unit of an element that retains its properties.'},
                {'term': 'Molecule', 'definition': 'A group of atoms bonded together.'},
                {'term': 'Chemical Reaction', 'definition': 'A process that changes substances into new ones.'}
            ]
        elif lesson.subject == 'history':
            sample_flashcards = [
                {'term': 'Civilization', 'definition': 'A complex society with cities, government, and culture.'},
                {'term': 'Empire', 'definition': 'A group of nations or peoples ruled by a single authority.'},
                {'term': 'Archaeology', 'definition': 'The study of ancient cultures through artifacts and remains.'}
            ]
        else:
            sample_flashcards = [
                {'term': 'Plot', 'definition': 'The sequence of events that make up a story.'},
                {'term': 'Character', 'definition': 'A person, animal, or being in a story.'},
                {'term': 'Setting', 'definition': 'The time and place where a story takes place.'}
            ]
        
        for flashcard_data in sample_flashcards:
            flashcard = Flashcard(
                term=flashcard_data['term'],
                definition=flashcard_data['definition'],
                lesson_id=lesson.id,
                ai_generated=False
            )
            db.session.add(flashcard)
        
        # Create sample questions for each lesson
        if lesson.subject == 'mathematics':
            sample_questions = [
                {
                    'question_text': 'What is the value of x in the equation 2x + 5 = 13?',
                    'answer_text': 'x = 4',
                    'question_type': 'multiple_choice'
                },
                {
                    'question_text': 'Simplify the expression 3x + 2x - x',
                    'answer_text': '4x',
                    'question_type': 'multiple_choice'
                }
            ]
        elif lesson.subject == 'science':
            sample_questions = [
                {
                    'question_text': 'What is the chemical symbol for gold?',
                    'answer_text': 'Au',
                    'question_type': 'multiple_choice'
                },
                {
                    'question_text': 'How many protons does a hydrogen atom have?',
                    'answer_text': '1',
                    'question_type': 'multiple_choice'
                }
            ]
        else:
            sample_questions = [
                {
                    'question_text': 'What is the main purpose of creative writing?',
                    'answer_text': 'To express imagination and creativity through words',
                    'question_type': 'essay'
                }
            ]
        
        for question_data in sample_questions:
            question = Question(
                question_text=question_data['question_text'],
                answer_text=question_data['answer_text'],
                question_type=question_data['question_type'],
                lesson_id=lesson.id,
                ai_generated=False
            )
            db.session.add(question)
    
    try:
        db.session.commit()
        print("Sample lessons created successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating sample lessons: {e}")

@lessons_bp.route('/')
def index():
    """
    Lessons index page showing all available lessons.
    Supports filtering by subject, age group, and difficulty.
    """
    
    # Create sample lessons if none exist
    create_sample_lessons()
    
    # Get filter parameters
    subject = request.args.get('subject', 'all')
    age_group = request.args.get('age_group', 'all')
    difficulty = request.args.get('difficulty', 'all')
    search_query = request.args.get('q', '').strip()
    
    # Build query
    query = Lesson.query.filter_by(is_published=True)
    
    if subject != 'all':
        query = query.filter(Lesson.subject == subject)
    
    if age_group != 'all':
        query = query.filter(Lesson.age_group_target == age_group)
    
    if difficulty != 'all':
        query = query.filter(Lesson.difficulty_level == difficulty)
    
    if search_query:
        query = query.filter(
            db.or_(
                Lesson.title.contains(search_query),
                Lesson.description.contains(search_query),
                Lesson.topic.contains(search_query),
                Lesson.tags.contains([search_query])
            )
        )
    
    # Get lessons with pagination
    page = request.args.get('page', 1, type=int)
    per_page = 12
    lessons = query.order_by(Lesson.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Get available filters
    subjects = db.session.query(Lesson.subject).distinct().all()
    age_groups = db.session.query(Lesson.age_group_target).distinct().all()
    difficulty_levels = db.session.query(Lesson.difficulty_level).distinct().all()
    
    return render_template('lessons/index.html',
                         lessons=lessons,
                         subjects=[s[0] for s in subjects],
                         age_groups=[ag[0].value for ag in age_groups],
                         difficulty_levels=[dl[0] for dl in difficulty_levels],
                         current_filters={
                             'subject': subject,
                             'age_group': age_group,
                             'difficulty': difficulty,
                             'search': search_query
                         })

@lessons_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """
    Lesson creation page with AI-powered content processing.
    Supports multiple input formats and age-adaptive content generation.
    """
    
    if not current_user.is_teacher():
        flash('Only teachers can create lessons.', 'error')
        return redirect(url_for('lessons.index'))
    
    if request.method == 'POST':
        # Handle lesson creation via AJAX
        return jsonify({'success': True, 'message': 'Lesson creation handled by AI services'})
    
    return render_template('lessons/create.html')

@lessons_bp.route('/<int:lesson_id>')
def view(lesson_id):
    """
    Lesson viewing page with age-adaptive interface.
    Shows lesson content, flashcards, and questions.
    """
    
    lesson = Lesson.query.get_or_404(lesson_id)
    
    if not lesson.is_published and (not current_user.is_authenticated or 
                                   current_user.id != lesson.teacher_id):
        flash('This lesson is not available.', 'error')
        return redirect(url_for('lessons.index'))
    
    # Get lesson content
    flashcards = lesson.flashcards.all()
    questions = lesson.questions.all()
    
    # Track engagement if user is logged in
    if current_user.is_authenticated:
        track_engagement(current_user.id, 'lesson_view', lesson_id)
    
    # Get user's age group for interface adaptation
    user_age_group = current_user.age_group.value if current_user.is_authenticated else None
    
    return render_template('lessons/view.html',
                         lesson=lesson,
                         flashcards=flashcards,
                         questions=questions,
                         user_age_group=user_age_group)

@lessons_bp.route('/<int:lesson_id>/edit')
@login_required
def edit(lesson_id):
    """
    Lesson editing page for teachers.
    """
    
    lesson = Lesson.query.get_or_404(lesson_id)
    
    if current_user.id != lesson.teacher_id and not current_user.role.value == 'admin':
        flash('You can only edit your own lessons.', 'error')
        return redirect(url_for('lessons.view', lesson_id=lesson_id))
    
    return render_template('lessons/edit.html', lesson=lesson)

@lessons_bp.route('/<int:lesson_id>/flashcards')
def flashcards(lesson_id):
    """
    Flashcards page for a specific lesson.
    Supports interactive learning and progress tracking.
    """
    
    lesson = Lesson.query.get_or_404(lesson_id)
    
    if not lesson.is_published and (not current_user.is_authenticated or 
                                   current_user.id != lesson.teacher_id):
        flash('This lesson is not available.', 'error')
        return redirect(url_for('lessons.index'))
    
    flashcards = lesson.flashcards.all()
    
    # Track engagement if user is logged in
    if current_user.is_authenticated:
        track_engagement(current_user.id, 'flashcard_review', lesson_id)
    
    return render_template('lessons/flashcards.html',
                         lesson=lesson,
                         flashcards=flashcards)

@lessons_bp.route('/<int:lesson_id>/questions')
def questions(lesson_id):
    """
    Practice questions page for a specific lesson.
    Supports different question types and difficulty levels.
    """
    
    lesson = Lesson.query.get_or_404(lesson_id)
    
    if not lesson.is_published and (not current_user.is_authenticated or 
                                   current_user.id != lesson.teacher_id):
        flash('This lesson is not available.', 'error')
        return redirect(url_for('lessons.index'))
    
    questions = lesson.questions.all()
    
    # Track engagement if user is logged in
    if current_user.is_authenticated:
        track_engagement(current_user.id, 'quiz_attempt', lesson_id)
    
    return render_template('lessons/questions.html',
                         lesson=lesson,
                         questions=questions)

@lessons_bp.route('/<int:lesson_id>/quiz')
def quiz(lesson_id):
    """
    Interactive quiz page for a specific lesson.
    Supports multiple question types and scoring.
    """
    
    lesson = Lesson.query.get_or_404(lesson_id)
    
    if not lesson.is_published and (not current_user.is_authenticated or 
                                   current_user.id != lesson.teacher_id):
        flash('This lesson is not available.', 'error')
        return redirect(url_for('lessons.index'))
    
    questions = lesson.questions.all()
    
    return render_template('lessons/quiz.html',
                         lesson=lesson,
                         questions=questions)

@lessons_bp.route('/<int:lesson_id>/submit-quiz', methods=['POST'])
@login_required
def submit_quiz(lesson_id):
    """
    Submit quiz answers and track performance.
    """
    
    try:
        lesson = Lesson.query.get_or_404(lesson_id)
        answers = request.json.get('answers', {})
        
        # Calculate score
        total_questions = len(answers)
        correct_answers = 0
        
        for question_id, answer in answers.items():
            question = Question.query.get(question_id)
            if question and question.answer_text.lower().strip() == answer.lower().strip():
                correct_answers += 1
        
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        # Create revision log
        revision_log = RevisionLog(
            user_id=current_user.id,
            lesson_id=lesson_id,
            score=score,
            revision_type='quiz',
            notes=f'Quiz completed with {correct_answers}/{total_questions} correct answers'
        )
        
        db.session.add(revision_log)
        db.session.commit()
        
        # Track engagement
        track_engagement(current_user.id, 'quiz_attempt', lesson_id, {
            'score': score,
            'questions_answered': total_questions
        })
        
        return jsonify({
            'success': True,
            'score': score,
            'correct_answers': correct_answers,
            'total_questions': total_questions,
            'message': f'Quiz completed! Score: {score:.1f}%'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@lessons_bp.route('/<int:lesson_id>/download')
@login_required
def download(lesson_id):
    """
    Download lesson content for offline use.
    Supports multiple formats and content packaging.
    """
    
    lesson = Lesson.query.get_or_404(lesson_id)
    
    if not lesson.is_published and current_user.id != lesson.teacher_id:
        flash('This lesson is not available for download.', 'error')
        return redirect(url_for('lessons.view', lesson_id=lesson_id))
    
    # Track download engagement
    track_engagement(current_user.id, 'download', lesson_id)
    
    # For now, return a simple text download
    # In production, implement proper content packaging
    content = f"""
EduMorph Lesson: {lesson.title}
Topic: {lesson.topic}
Subject: {lesson.subject}
Duration: {lesson.estimated_duration} minutes

Summary:
{lesson.ai_summary}

Key Points:
"""
    
    for point in lesson.key_points or []:
        content += f"\n{point['id']}. {point['point']}"
    
    content += f"""

Flashcards:
"""
    
    for flashcard in lesson.flashcards:
        content += f"\nQ: {flashcard.term}\nA: {flashcard.definition}\n"
    
    content += f"""

Practice Questions:
"""
    
    for question in lesson.questions:
        content += f"\nQ: {question.question_text}\nA: {question.answer_text}\n"
    
    # Return as downloadable text file
    from flask import make_response
    response = make_response(content)
    response.headers['Content-Type'] = 'text/plain'
    response.headers['Content-Disposition'] = f'attachment; filename="{lesson.title}.txt"'
    
    return response

@lessons_bp.route('/<int:lesson_id>/api/progress')
@login_required
def api_progress(lesson_id):
    """
    API endpoint for lesson progress tracking.
    """
    
    try:
        # Get user's progress for this lesson
        revision_logs = RevisionLog.query.filter_by(
            user_id=current_user.id,
            lesson_id=lesson_id
        ).order_by(RevisionLog.timestamp.desc()).all()
        
        if not revision_logs:
            return jsonify({
                'success': True,
                'progress': {
                    'completed': False,
                    'score': 0,
                    'attempts': 0,
                    'last_attempt': None
                }
            })
        
        latest_log = revision_logs[0]
        total_attempts = len(revision_logs)
        
        progress = {
            'completed': latest_log.score >= 70,  # 70% threshold for completion
            'score': latest_log.score,
            'attempts': total_attempts,
            'last_attempt': latest_log.timestamp.isoformat(),
            'best_score': max(log.score for log in revision_logs),
            'average_score': sum(log.score for log in revision_logs) / total_attempts
        }
        
        return jsonify({
            'success': True,
            'progress': progress
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@lessons_bp.route('/<int:lesson_id>/api/flashcards')
def api_flashcards(lesson_id):
    """
    API endpoint for lesson flashcards.
    """
    
    try:
        lesson = Lesson.query.get_or_404(lesson_id)
        flashcards = lesson.flashcards.all()
        
        flashcard_data = []
        for flashcard in flashcards:
            flashcard_data.append({
                'id': flashcard.id,
                'term': flashcard.term,
                'definition': flashcard.definition,
                'context': flashcard.context,
                'example': flashcard.example
            })
        
        return jsonify({
            'success': True,
            'flashcards': flashcard_data,
            'total': len(flashcard_data)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@lessons_bp.route('/<int:lesson_id>/api/questions')
def api_questions(lesson_id):
    """
    API endpoint for lesson questions.
    """
    
    try:
        lesson = Lesson.query.get_or_404(lesson_id)
        questions = lesson.questions.all()
        
        question_data = []
        for question in questions:
            question_data.append({
                'id': question.id,
                'question': question.question_text,
                'answer': question.answer_text,
                'type': question.question_type,
                'difficulty': question.difficulty_level
            })
        
        return jsonify({
            'success': True,
            'questions': question_data,
            'total': len(question_data)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def track_engagement(user_id, activity_type, lesson_id, additional_data=None):
    """
    Track user engagement with lessons.
    """
    
    try:
        engagement = EngagementMetric(
            user_id=user_id,
            activity_type=activity_type,
            activity_data={
                'lesson_id': lesson_id,
                'additional_data': additional_data or {}
            }
        )
        
        db.session.add(engagement)
        db.session.commit()
        
    except Exception as e:
        print(f"Error tracking engagement: {e}")
        db.session.rollback()

@lessons_bp.route('/api/recommendations')
@login_required
def api_recommendations():
    """
    API endpoint for personalized lesson recommendations.
    """
    
    try:
        # Get user's learning history
        user_revision_logs = RevisionLog.query.filter_by(
            user_id=current_user.id
        ).order_by(RevisionLog.timestamp.desc()).limit(10).all()
        
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
            db.or_(
                Lesson.subject.in_(list(studied_subjects)),
                Lesson.topic.in_(list(studied_topics))
            )
        ).filter(Lesson.id.notin_([log.lesson_id for log in user_revision_logs])).limit(6).all()
        
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
                'url': url_for('lessons.view', lesson_id=lesson.id)
            })
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'total': len(recommendations)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
