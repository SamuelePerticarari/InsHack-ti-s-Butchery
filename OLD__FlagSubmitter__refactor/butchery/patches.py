from auth import is_logged
from challenges import get_challenges
from database import get_db
from datetime import datetime
from flask import (
    Blueprint, current_app as app, flash, g, redirect, render_template, request, url_for
)
import os
from utils import get_random_string
from werkzeug.utils import secure_filename

bp = Blueprint('patches', __name__, url_prefix='/patches')


@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('patches.html', CHALLENGES_DATA=get_challenges(), PATCHES_DATA=get_patches())


@bp.route('/add-patch', methods=('GET', 'POST'))
def add_patch():
    if g.user is None:
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        return render_template('add-patch.html', CHALLENGES_DATA=get_challenges(), PATCHES_DATA=get_patches())

    if request.method == 'POST':
        user_id = g.user[0]
        challenge_id = request.form['challenge_id']
        patch_name = request.form['patch_name']
        patch_version = request.form['patch_version']
        patch_description = request.form['patch_description']
        patch_files = request.files.getlist("patch_files[]")

        db = get_db()
        error = None
        error_file = False

        if not patch_name:
            patch_name = '-'

        if not challenge_id:
            error = 'Challenge id is required.'
        elif not patch_description:
            error = 'Description is required.'
        elif not patch_version:
            error = 'Version is required.'
        elif not patch_files or len(patch_files) is 0:
            error = 'Files are required.'
            error_file = True
        elif not user_id:
            error = 'User id is required.'

        patches_paths = []

        if error_file is False:
            base_path = app.config['UPLOADS_FOLDER'] + get_random_string(15) + '/'

            os.mkdir(base_path, 0777)

            # Sandbox installation
            #
            # uid = pwd.getpwnam('InsHackSandbox').pw_uid
            # gid = grp.getgrnam('InsHackSandbox').gr_gid
            #
            # os.chown( base_path, uid, gid)
            # os.chmod( base_path, 0777 )

            for patch_file in patch_files:
                patch_path = base_path + secure_filename(patch_file.filename)
                patch_file.save(patch_path)
                patches_paths.append(patch_path)

                # Sandbox installation
                #
                # os.chown( patch_path, uid, gid)
                # os.chmod( patch_path, 0777 )
                #
                # print patch_path

        if error is None:
            db.execute(
                'INSERT INTO patches (name, version, description, path, user_id, challenge_id) ' +
                'VALUES (?, ?, ?, ?, ?, ?)',
                (patch_name, patch_version, patch_description, '-_-*+*-_-'.join(patches_paths), user_id, challenge_id)
            )
            db.commit()
            msg = "Patch uploaded. ({})".format('\n    '.join(patches_paths))

            return render_template('add-patch.html', message=msg, CHALLENGES_DATA=get_challenges(),
                                   PATCHES_DATA=get_patches())

        flash(error)

        return redirect(url_for('patches.add_patch', CHALLENGES_DATA=get_challenges(), PATCHES_DATA=get_patches()))


def get_patches():
    if not is_logged():
        return redirect(url_for('auth.login'))

    final_view = []

    challenges = get_db().execute(
        'SELECT name, port FROM challenges'
    ).fetchall()

    for challenge in challenges:
        challenge_name = challenge[0]
        challenge_port = challenge[1]

        challenge_data = {
            'challenge_name': challenge_name,
            'challenge_port': challenge_port,
            'patches': []
        }
        final_view.append(challenge_data)

    challenge_patches = get_db().execute(
        'SELECT C.name, C.port, P.id, P.name, P.version, P.description, P.path, P.timestamp, U.username ' +
        'FROM challenges AS C, patches AS P, users AS U ' +
        'WHERE C.id = P.challenge_id AND P.user_id = U.id ' +
        'ORDER BY P.timestamp DESC'
    ).fetchall()

    for challenge_patch in challenge_patches:
        challenge_name = challenge_patch[0]
        challenge_port = challenge_patch[1]
        patch_id = challenge_patch[2]
        name = challenge_patch[3]
        version = challenge_patch[4]
        description = challenge_patch[5]
        path = challenge_patch[6]
        timestamp = challenge_patch[7]
        owner_username = challenge_patch[8]

        patch_data = {
            'id': patch_id,
            'name': name,
            'version': version,
            'description': description,
            'path': path,
            'timestamp': datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S'),
            'owner': owner_username
        }

        patch_inserted = False

        for item in final_view:
            if item['challenge_name'] == challenge_name and item['challenge_port'] == challenge_port:
                item['patches'].append(patch_data)
                patch_inserted = True

        if not patch_inserted:
            challenge_data = {
                'challenge_name': challenge_name,
                'challenge_port': challenge_port,
                'patches': [patch_data]
            }

            final_view.append(challenge_data)

    return final_view
