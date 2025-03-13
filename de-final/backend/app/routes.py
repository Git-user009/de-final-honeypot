from flask import request, jsonify
from flask_login import login_user, login_required, current_user
from .models import User
from . import db

# Create a Blueprint for the routes
from flask import Blueprint
main = Blueprint('main', __name__)

# Login Endpoint
@main.route('/api/login', methods=['POST'])
def login():
    """
    Authenticate a user and log them in.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    print(f"🔍 Debug: Received login request - Username: {username}")

    # Find the user in the database
    user = User.query.filter_by(username=username).first()

    if not user:
        print("❌ Debug: User not found in database")
        return jsonify({'error': 'Invalid username or password'}), 401

    # Check if password is correct
    if not user.check_password(password):
        print("❌ Debug: Password mismatch")
        print(f"🔍 Entered Password: {password}")
        print(f"🔍 Stored Hash: {user.password_hash}")
        return jsonify({'error': 'Invalid username or password'}), 401

    print("✅ Debug: Login successful")
    login_user(user)
    return jsonify({'message': 'Login successful', 'role': user.role}), 200

# Registration Endpoint
@main.route('/api/register', methods=['POST'])
def register():
    """
    Register a new admin user (no authentication required for simplicity).
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'admin')  # Default to admin

    # Validate input
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    # Check if the username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    # Create and save the new user
    new_user = User(username=username, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Admin registered successfully'}), 201

# Admin: Create Users
@main.route('/api/create-user', methods=['POST'])
@login_required
def create_user():
    """
    Create a new user (admin only).
    """
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    # Validate input
    if not username or not password or not role:
        return jsonify({'error': 'Missing username, password, or role'}), 400

    # Check if the username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    # Create and save the new user
    new_user = User(username=username, role=role)
    new_user.set_password(password)  # Hash the password
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

# Admin: Block IPs
@main.route('/api/block-ip', methods=['POST'])
@login_required
def block_ip():
    """
    Block an IP address (admin only).
    """
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    ip = data.get('ip')

    # Add logic to block the IP (e.g., store in a blocked_ips table)
    # Example: blocked_ips.add(ip)
    return jsonify({'message': f'IP {ip} blocked'})

# Admin: Delete Users
@main.route('/api/delete-user', methods=['POST'])
@login_required
def delete_user():
    """
    Delete a user (admin only).
    """
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    user_id = data.get('user_id')

    # Find the user
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'})

# Admin: Reset Passwords
@main.route('/api/reset-password', methods=['POST'])
@login_required
def reset_password():
    """
    Reset a user's password (admin only).
    """
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    user_id = data.get('user_id')
    new_password = data.get('new_password')

    # Validate input
    if not user_id or not new_password:
        return jsonify({'error': 'Missing user ID or new password'}), 400

    # Find the user
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Reset the password
    user.set_password(new_password)  # Hash the new password
    db.session.commit()

    return jsonify({'message': 'Password reset successfully'})