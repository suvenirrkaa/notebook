from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from db.session import SessionLocal, engine
from db.models import Base
from db.models.user import User
from db.models.note import Note
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.secret_key = 'hncdfi7843b'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    session = SessionLocal()
    return session.query(User).get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    session = SessionLocal()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if session.query(User).filter_by(username=username).first():
            flash('')
            return redirect(url_for('register'))
        
        user = User(username=username)
        user.set_password(password)
        session.add(user)
        session.commit()
        flash('')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    session = SessionLocal()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = session.query(User).filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('notes'))
        flash('')
    return render_template('login.html')
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    session = SessionLocal()
    if request.method == 'POST':
        content = request.form['content']
        note = Note(content=content, user=current_user)
        session.add(note)
        session.commit()
        return redirect(url_for('notes'))
    
    notes = session.query(Note).filter_by(user_id=current_user.id).all()
    return render_template('notes.html', notes=notes)

with app.app_context():
    Base.metadata.create_all(bind=engine)
    
    
if __name__ == '__main__':
    app.run(debug=True)
