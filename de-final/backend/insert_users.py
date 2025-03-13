from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Rollback any existing transaction
    db.session.rollback()

    # Check for existing users
    existing_admin = User.query.filter_by(username='admin').first()
    existing_analyst = User.query.filter_by(username='analyst').first()

    if existing_admin:
        print("Admin user already exists! Deleting...")
        db.session.delete(existing_admin)
    if existing_analyst:
        print("Analyst user already exists! Deleting...")
        db.session.delete(existing_analyst)
    db.session.commit()

    # Create and insert new users
    admin = User(username='admin', role='admin')
    admin.set_password('admin_password')  # Hash the password

    analyst = User(username='analyst', role='analyst')
    analyst.set_password('analyst_password')  # Hash the password

    db.session.add(admin)
    db.session.add(analyst)
    db.session.commit()

    print("Users added successfully!")