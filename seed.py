"""
Seed script for EduMorph
Creates sample users (student, teacher, parent, admin) and lessons for testing dashboards and features.
"""

from app import create_app, db
from database.models import User, UserRole, AgeGroup, Lesson
from werkzeug.security import generate_password_hash

app = create_app('development')

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create sample users
    users = [
        User(username='student1', email='student1@example.com', password_hash=generate_password_hash('password'), role=UserRole.student, age_group=AgeGroup.children),
        User(username='teacher1', email='teacher1@example.com', password_hash=generate_password_hash('password'), role=UserRole.teacher, age_group=AgeGroup.young_adults),
        User(username='parent1', email='parent1@example.com', password_hash=generate_password_hash('password'), role=UserRole.parent, age_group=AgeGroup.adults),
        User(username='admin1', email='admin1@example.com', password_hash=generate_password_hash('password'), role=UserRole.admin, age_group=AgeGroup.adults)
    ]
    db.session.add_all(users)

    # Create sample lessons
    lessons = [
        Lesson(title='Math Basics', description='Introduction to basic math concepts.', age_group_target='children', is_published=True),
        Lesson(title='Physics for Teens', description='Fundamentals of physics for teenagers.', age_group_target='teens', is_published=True),
        Lesson(title='Career Skills', description='Professional skills for young adults.', age_group_target='young_adults', is_published=True),
        Lesson(title='Financial Literacy', description='Money management for adults.', age_group_target='adults', is_published=True)
    ]
    db.session.add_all(lessons)

    db.session.commit()
    print('✅ Database seeded with sample users and lessons.')
