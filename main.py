from note import app, db
from note.model import User
from werkzeug.security import generate_password_hash

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', password=generate_password_hash('admin123'))
            db.session.add(admin_user)
            db.session.commit()
    app.run(host='127.0.0.1', port=5000)
