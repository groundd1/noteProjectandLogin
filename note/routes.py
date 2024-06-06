from flask import render_template, request, redirect, url_for, flash, session
from note import app, db
from note.model import NoteEntry, User
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError


@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    entries = NoteEntry.query.filter_by(user_id=user_id).all()

    topics = {'work': [], 'personal': [], 'other': []}
    for entry in entries:
        if entry.topic in topics:
            topics[entry.topic].append(entry)
        else:
            topics['other'].append(entry)

    return render_template('index.html', topics=topics)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            flash('Incorrect username or password.')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = 'Username already exists.'
        else:
            new_user = User(username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful.')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['createTitle']
        date = request.form['createDate']
        text = request.form['createText']
        topic = request.form['createTopic']
        user_id = session['user_id']

        if len(title) > 8:
            title = title[:8] + '...'

        new_entry = NoteEntry(title=title, date=date, text=text, user_id=user_id, topic=topic)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit(entry_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    entry = NoteEntry.query.filter_by(id=entry_id, user_id=session['user_id']).first()
    if request.method == 'POST':
        entry.title = request.form['editTitle']
        entry.date = request.form['editDate']
        entry.text = request.form['editText']
        entry.topic = request.form['editTopic']
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except SQLAlchemyError:
            db.session.rollback()
            flash('Error updating entry.')
            return redirect(url_for('edit', entry_id=entry_id))
    return render_template('edit.html', entry=entry)


@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete(entry_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    entry = NoteEntry.query.filter_by(id=entry_id, user_id=session['user_id']).first()
    try:
        db.session.delete(entry)
        db.session.commit()
        return redirect(url_for('index'))
    except SQLAlchemyError:
        db.session.rollback()
        flash('Error deleting entry.')
        return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')
