from exploits import get_exploits
from flags import get_flags
from flask import (
    Blueprint, current_app as app, g, redirect, render_template, request, url_for, send_file
)
import os
from patches import get_patches
from teams import get_teams

bp = Blueprint('base', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    if g.user is not None:
        return redirect(url_for('base.dashboard'))

    return 'Don\'t hack this please.'


@bp.route('/dashboard', methods=('GET', 'POST'))
def dashboard():
    if g.user is None:
        return redirect(url_for('base.index'))

    return render_template('dashboard.html', EXPLOITS_DATA=get_exploits(), TEAMS_DATA=get_teams(),
                           FLAGS_DATA=get_flags(), PATCHES_DATA=get_patches())


@bp.route('/get-file', methods=('GET', 'POST'))
def get_file():
    if g.user is None:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        path = request.form['path']

        if len(path) == 0:
            return redirect(url_for('base.dashboard'))

        if len(path) == 0:
            return redirect(url_for('base.dashboard'))

        if path[0:8] != app.config['UPLOADS_FOLDER']:
            path = app.config['UPLOADS_FOLDER'] + path

        if len(path) == 0:
            return redirect(url_for('base.dashboard'))

        while '../' in path:
            path = path.replace('../', '')

        if path[0] == '/':
            path = path[1:]

        try:
            return send_file(os.getcwd() + '/' + path, as_attachment=True)
        except Exception as e:
            return 'Error: {}'.format(e)

    return redirect(url_for('base.dashboard'))
