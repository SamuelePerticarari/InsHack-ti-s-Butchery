from database import get_db
from flags import get_flags
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from patches import get_patches

bp = Blueprint('teams', __name__, url_prefix='/teams')


@bp.route('/add-team', methods=('GET', 'POST'))
def add_team():
    if g.user is None:
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        return render_template('add-team.html', TEAMS_DATA=get_teams(), FLAGS_DATA=get_flags(),
                               PATCHES_DATA=get_patches())

    if request.method == 'POST':
        team_name = request.form['team_name']
        team_ip = request.form['team_ip']

        db = get_db()
        error = None

        if not team_name:
            error = 'Name is required.'
        elif not team_ip:
            error = 'Team ip is required.'
        elif db.execute(
                'SELECT id FROM teams WHERE name = ? OR ip = ?', (team_name, team_ip)
        ).fetchone() is not None:
            error = '{} ({}) is already present.'.format(team_name, team_ip)

        if error is None:
            db.execute(
                'INSERT INTO teams (name, ip) VALUES (?, ?)', (team_name, team_ip)
            )
            db.commit()
            msg = "Team created. {} ({})".format(team_name, team_ip)
            return render_template('add-team.html', message=msg, TEAMS_DATA=get_teams(), FLAGS_DATA=get_flags(),
                                   PATCHES_DATA=get_patches())

        flash(error)

        return redirect(
            url_for('teams.add_team', TEAMS_DATA=get_teams(), FLAGS_DATA=get_flags(), PATCHES_DATA=get_patches()))


@bp.route('/toggle-team', methods=('GET', 'POST'))
def toggle_team():
    if g.user is None:
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        return redirect(url_for('base.dashboard'))

    if request.method == 'POST':
        team_id = request.form['team_id']

        if team_id:
            db = get_db()
            db.execute(
                'UPDATE teams SET enabled = not enabled WHERE id = ?', (team_id,)
            )
            db.commit()

        return redirect(url_for('base.dashboard'))


def get_teams():
    db = get_db()
    return db.execute(
        'SELECT id, name, ip, enabled FROM teams',
    ).fetchall()
