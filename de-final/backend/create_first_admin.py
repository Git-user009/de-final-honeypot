from app import create_app, db
from app.models import User

app = create_app()

def create_first_admin():
    with app.app_context():
        # Check if an admin user already exists
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("Admin user already exists!")
        else:
            # Create the admin user
            admin = User(username='admin', role='admin')
            admin.set_password('admin_password')  # Hash the password
            db.session.add(admin)
            db.session.commit()
            print("First admin created successfully!")

if __name__ == '__main__':
    create_first_admin()