"""
Production admin user creation script
"""
from app import app, db, User
import getpass

def create_admin():
    with app.app_context():
        print("=== WhatsFlow Admin User Creation ===\n")
        
        email = input("Enter admin email: ").strip()
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"\nUser with email '{email}' already exists!")
            update = input("Do you want to update the password? (yes/no): ").strip().lower()
            if update != 'yes':
                print("Operation cancelled.")
                return
            user = existing_user
        else:
            user = User(email=email, is_admin=True)
        
        # Get password securely
        while True:
            password = getpass.getpass("Enter admin password (min 8 characters): ")
            if len(password) < 8:
                print("Password must be at least 8 characters long!")
                continue
            
            confirm = getpass.getpass("Confirm password: ")
            if password != confirm:
                print("Passwords do not match!")
                continue
            
            break
        
        # Set password and save
        user.set_password(password)
        if not existing_user:
            db.session.add(user)
        db.session.commit()
        
        print(f"\n✓ Admin user '{email}' created successfully!")
        print("You can now log in to the admin panel.")

if __name__ == '__main__':
    create_admin()
