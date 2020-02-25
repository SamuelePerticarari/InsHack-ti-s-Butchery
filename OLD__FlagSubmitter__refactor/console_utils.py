import imp
import os

VERBOSE = False

# load database module
database = imp.load_source('*', 'butchery/database.py')
DB = database.connect_to_db('instance/InsHack@ti.sqlite')

BASE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'


def active_teams(teams):
    """
    Read provided teams and return active ones list
    """
    active = []

    for team in teams:
        if team['enabled']:
            active.append(team)

    return active


def get_teams():
    """
    Read teams from database and return structured array
    """
    teams = []
    data = DB.execute(
        'SELECT id, name, ip, enabled FROM teams'
    ).fetchall()

    for team in data:
        team_data = {
            'id': team[0],
            'name': team[1],
            'ip': team[2],
            'enabled': team[3]
        }
        teams.append(team_data)

    return teams


def get_challenges_exploits():
    """
    Read challenges and related exploits from database and return structured array\
    """
    final_view = []

    challenges = DB.execute(
        'SELECT name, port FROM challenges'
    ).fetchall()

    for challenge in challenges:
        challenge_name = challenge[0]
        challenge_port = challenge[1]

        challenge_data = {
            'challenge_name': challenge_name,
            'challenge_port': challenge_port,
            'exploits': []
        }
        final_view.append(challenge_data)

    exploits = DB.execute(
        'SELECT C.name, C.port, E.id, E.version, E.command, E.path, E.timestamp, E.enabled, U.username ' +
        'FROM challenges AS C, exploits AS E, users AS U ' +
        'WHERE C.id = E.challenge_id AND E.user_id = U.id AND E.enabled = 1'
    ).fetchall()

    for exploit in exploits:
        challenge_name = exploit[0]
        challenge_port = exploit[1]
        exploit_id = exploit[2]
        version = exploit[3]
        command = exploit[4]
        path = exploit[5]
        timestamp = exploit[6]
        enabled = exploit[7]
        owner_username = exploit[8]

        exploit_data = {
            'id': exploit_id,
            'version': version,
            'command': command,
            'base_dir': '/'.join(path.split('/')[:-1]) + '/',
            'path': path,
            'timestamp': timestamp,
            'enabled': enabled,
            'owner': owner_username
        }

        exploit_inserted = False

        for item in final_view:
            if item['challenge_name'] == challenge_name and item['challenge_port'] == challenge_port:
                item['exploits'].append(exploit_data)
                exploit_inserted = True

        if not exploit_inserted:
            challenge_data = {
                'challenge_name': challenge_name,
                'challenge_port': challenge_port,
                'exploits': [exploit_data]
            }
            final_view.append(challenge_data)

    return final_view


def cool_teams(teams):
    """
    Print teams in a cool way
    """
    print "-" * 100 + '-'
    print "|  {:60} | {:33} |".format("TEAM NAME", "IP")
    print "-" * 100 + '-'
    for team in teams:
        print "|  {:60} | {:33} |".format(team['name'].encode('utf-8'), team['ip'])
    print "-" * 100 + '-'
    print


def cool_challenges(challenges):
    """
    Print challenges in a cool way
    """
    print "-" * 100 + '-'
    print "|  {:40} | {:20} | {:30} |".format("CHALLENGE", "EXPLOITS", "PORT")
    print "-" * 100 + '-'
    for challenge in challenges:
        print "|  {:40} | {:20} | {:30} |".format(challenge['challenge_name'],
                                                  str(len(challenge['exploits'])) + ' exploits',
                                                  str(challenge['challenge_port']))
    print "-" * 100 + '-'
    print
