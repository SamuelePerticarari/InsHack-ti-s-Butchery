from database import get_db
from flask import (
    Blueprint, current_app as app, flash, g, redirect, render_template, request, session, url_for
)
import functools
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if app.config['LOCKED_REGISTRATION']:
        return 'Registration is not allowed.'
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        if not name:
            error = 'Name is required.'
        elif not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif len(password) < 8:
            error = 'Password must be longer than 7 characters.'
        elif db.execute(
                'SELECT id FROM users WHERE username = ? OR name = ?', (username, name)
        ).fetchone() is not None:
            error = '{} ({}) is already registered.'.format(username, name)
        if error is None:
            password_encrypted = generate_password_hash(password)
            db.execute(
                'INSERT INTO users (name, username, password) VALUES (?, ?, ?)', (name, username, password_encrypted)
            )
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)

    if g.user is None:
        return render_template('auth/register.html')

    return redirect(url_for('base.index'))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('base.index'))

        flash(error)

    if g.user is None:
        return render_template('auth/login.html')

    return redirect(url_for('base.index'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('base.index'))


@bp.before_app_request
def logged_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT id, name, username FROM users WHERE id = ?', (user_id,)
        ).fetchone()


def is_logged():
    user = session.get('user_id')
    if user is None:
        return False
    else:
        return True


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
