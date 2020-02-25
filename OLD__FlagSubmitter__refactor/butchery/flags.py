from database import get_db
from datetime import datetime
from flask import (
    Blueprint, render_template
)

bp = Blueprint('flags', __name__, url_prefix='/teams')


@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('flags.html', FLAGS_DATA=get_flags())


def get_flags():
    db = get_db()
    flags = db.execute(
        'SELECT F.id, F.flag, F.submitted, F.timestamp, T.name, C.name, C.port, U.username, E.version ' +
        'FROM challenges AS C, flags AS F, teams AS T, users AS U, exploits AS E ' +
        'WHERE F.team_id = T.id AND C.id = E.challenge_id AND U.id = E.user_id AND F.exploit_id = E.id ' +
        'ORDER BY F.id DESC'
    ).fetchall()

    final_view = []

    for flag in flags:
        flag_id = flag[0]
        flag_string = flag[1]
        submitted = flag[2]
        timestamp = flag[3]
        team_name = flag[4]
        challenge_name = flag[5]
        challenge_port = flag[6]
        exploit_owner_username = flag[7]
        exploit_version = flag[8]

        data = {
            'id': flag_id,
            'flag': flag_string,
            'submitted': submitted,
            'timestamp': datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S'),
            'team_name': team_name,
            'challenge_name': challenge_name,
            'challenge_port': challenge_port,
            'exploit_owner': exploit_owner_username,
            'exploit_version': exploit_version
        }
        final_view.append(data)

    return final_view
