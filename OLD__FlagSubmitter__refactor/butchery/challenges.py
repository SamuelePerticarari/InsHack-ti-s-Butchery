from auth import is_logged
from database import get_db
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

bp = Blueprint('challenges', __name__, url_prefix='/challenges')


@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('challenges.html', CHALLENGES_DATA=get_challenges())


@bp.route('/add-challenge', methods=('GET', 'POST'))
def add_challenge():
    if g.user is None:
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        return render_template('add-challenge.html', CHALLENGES_DATA=get_challenges())

    if request.method == 'POST':
        challenge_name = request.form['challenge_name']
        challenge_port = request.form['challenge_port']
        db = get_db()
        error = None

        if not challenge_name:
            error = 'Name is required.'
        elif not challenge_port:
            error = 'Port is required.'
        elif db.execute(
                'SELECT id FROM challenges WHERE name = ? AND port = ?', (challenge_name, challenge_port)
        ).fetchone() is not None:
            error = '{}:{} is already present.'.format(challenge_name, challenge_port)

        if error is None:
            db.execute(
                'INSERT INTO challenges (name, port) VALUES (?, ?)', (challenge_name, challenge_port)
            )
            db.commit()
            msg = "Challenge created. {}:{}".format(challenge_name, challenge_port)
            return render_template('add-challenge.html', message=msg, CHALLENGES_DATA=get_challenges())

        flash(error)

        return render_template('add-challenge.html', CHALLENGES_DATA=get_challenges())


@bp.route('/delete/<challenge_id>', methods=['GET'])
def delete_challenge(challenge_id):
    if not is_logged():
        return redirect(url_for('auth.login'))

    db = get_db()
    db.execute(
        'DELETE FROM challenges WHERE id = ?',
        (challenge_id,)
    )
    db.commit()

    return redirect(url_for('challenges.index'))


def get_challenges():
    db = get_db()
    return db.execute(
        'SELECT id, name, port FROM challenges',
    ).fetchall()
