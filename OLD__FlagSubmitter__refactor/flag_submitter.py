#!/usr/bin/python
import requests
import imp
import os
import re
import datetime
import time
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = 'https://10.20.0.1/submit'
# URL = 'http://127.0.0.1'
TEAM_TOKEN = 'eFMC6rVQalJiA6AS'


VERBOSE = False

if len( sys.argv ) >= 2:
    VERBOSE = (sys.argv[1].lower() == 'verbose')

InitialDir = os.getcwd()

# Carica modulo per database
database = imp.load_source('*', 'CTF-Flag-Submitter/database.py')
DB = database.connect_to_db( 'instance/InsHack@ti.sqlite' )

def SendFlag( FLAG ):

    try:
        # r = requests.post( URL, data={'team_token': TEAM_TOKEN, 'flag': FLAG}, verify=False )
        r = requests.post( URL, data={'team_token': TEAM_TOKEN, 'flag': FLAG}, verify=False )
    except Exception as e:
        print "ERROR: {}".format( str(e) )
        print ""
        return False

    text = r.text
    # print text# = r.text
    # print "===== RESPONSE FROM MASTER SERVER API ====="
    # print text
    # print "==========================================="

    if 'flag accepted!' in text.lower():
        print "Sent new flag: {}".format( FLAG )
        return True
    elif 'duplicated flag!' in text.lower():
        print "Duplicated flag: {}".format( FLAG )
        return True
    elif 'submitted flag is expired!' in text.lower():
        print "Expired flag: {}".format( FLAG )
        return True
    else:
        return False


# def SUBMIT_FILE():
#     pass
#     print "Open file."
#     with open('flags.txt', 'r') as f:
#         for xx in f.readlines():
#             if len(xx) > 0:
#                 print "FROM FILE: FLAG: {}".format( xx )
#                 res = SendFlag(xx)
#
#     with open('flags.txt', 'w') as f:
#         f.write('\n')

def main():

    i = 1

    while True:

        # SUBMIT_FILE()

        # os.system('clear')
        print "Flag Submitter - Loop n. {}".format(i)

        init_time = time.time()

        flags = DB.execute(
            'SELECT id, flag FROM flags ' + 'WHERE already_submitted = 0'
        ).fetchall()

        for flag_result in flags:
            id = flag_result[0]
            flag = flag_result[1]
            res = SendFlag(flag)
            if res:
                DB.execute(
                    'UPDATE flags SET already_submitted = 1 WHERE id = ?',
                    (id,)
                )
                DB.commit()


        end_time = time.time()

        while (end_time - init_time < 6):
            end_time = time.time()
            time.sleep(1)

        i+=1



if __name__ == '__main__':
    main()
