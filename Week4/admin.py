import os
from models import User
from extensions import db, bcrypt

def create_first_admin(app):
    if os.getenv('ADMIN_EMAIL') and os.getenv('ADMIN_PASSWORD'):
        with app.app_context():
            # only create one admin
            if not User.query.filter_by(role='admin').first():
                hashed = bcrypt.generate_password_hash(os.getenv('ADMIN_PASSWORD')).decode('utf-8')
                admin = User(
                    username='admin1',
                    email=os.getenv('ADMIN_EMAIL'),
                    password=hashed,
                    role='admin'
                )
                db.session.add(admin)
                db.session.commit()
                app.logger.info('First admin created.')