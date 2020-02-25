from ExploitManager.ConfigurationParser.configuration_parser import ConfigurationParser
from ExploitManager.Database.drivers.sqlite import *
from time import time, sleep
from pynotifier import Notification
from requests import post
from math import floor

def get_base_folder():
    from os.path import dirname, abspath
    return abspath( dirname( abspath(__file__) ) + '/../' )

class FlagSubmitter(object):
    """docstring for FlagSubmitter."""

    def __init__(self, argv):
        super(FlagSubmitter, self).__init__()
        self.verbose = False
        self.DELTA_TIME = 6
        config_path = get_base_folder() + '/config.json'
        self.configs = ConfigurationParser(config_path).get_configs()

        self.event = self.configs['event']
        self.master_url = self.configs['master_url']
        self.TEAM_TOKEN = self.configs['token']
        self.argv = argv
        self.db = Sqlite_DB_Driver(
            path=get_base_folder() + '/DB/InsHack@ti.sqlite',
            setup_path_schema=get_base_folder() + '/DB/InsHack@ti.sql'
        )


    def run(self):
        self.db.connect_to_db()
        i = 1
        self.last__flag_check_time = time()
        self.last__flag_count = self.db.count_flags()
        while True:
            init_time = time()
            print( "Loop n. {}".format( str(i).rjust(6, ' ') ), flush=True )

            self.check_heartbeat()

            self.tick()

            end_time = time()
            s = ''
            while (end_time - init_time < self.DELTA_TIME):
                end_time = time()
                s = "Waiting... ( {} / {} )".format( floor((end_time - init_time)*1000)/1000, self.DELTA_TIME )
                print(s, end='\b'*len(s), flush=True)
                sleep(0.5)
            # Clear line
            print('{}{}'.format(' '*len(s), '\b'*len(s)), end='', flush=True)
            i+=1

    def tick(self):
        flags_data = self.db.list_flags_not_submitted()

        for flag_data in flags_data:
            res = self.send_flag(flag_data)
            self.db.set_flag_status( id=flag_data['id'], status=res['status'], submitted=res['submitted'] )
            pass

    def send_flag(self, flag_data):
        ret = {
            'status': '',
            'submitted': False
        }
        sent = False
        n_retries = 5
        # Riprova 5 volte
        for i in range(n_retries):
            try:
                data = {
                    'team_token': self.TEAM_TOKEN,
                    'flag': flag_data['flag']
                }

                r = post( self.master_url, data=data, verify=False )
                text = r.text
                sent = True
                break
            except Exception as e:
                print("Errore: {}".format( str(e) ))


        ret['submitted'] = sent

        if sent is not True:
            Notification(
                title='FLAG {} NON INVIATO!'.format(flag_data['flag']),
                description='L\'invio della richiesta POST è fallita per {} volte...'.format(n_retries),
                icon_path=get_base_folder() + '/InsHack@ti.jpg', # On Windows .ico is required, on Linux - .png
                duration=self.DELTA_TIME,                              # Duration in seconds
                urgency=Notification.URGENCY_CRITICAL
            ).send()
            ret['status'] = "NETWORK ERROR"
            return ret

        # print "===== RESPONSE FROM MASTER SERVER API ====="
        # print text
        # print "==========================================="

        if 'accepted' in text.lower():
            print("[SENT]       {}".format( flag_data['flag'] ))
            ret['status'] = "SENT"
        elif 'duplicated' in text.lower():
            print("[DUPLICATED] {}".format( flag_data['flag'] ))
            ret['status'] = "DUPLICATED"
        elif 'expired' in text.lower():
            print("[EXPIRED]    {}".format( flag_data['flag'] ))
            ret['status'] = "EXPIRED"
        else:
            print("UNKNOWN ERROR. Response: {}".format(text))
            print("Flag: {}".format( flag_data['flag'] ))
            ret['status'] = "UNKNOWN ERROR. Response: {}".format(text)

        return ret

    def check_heartbeat(self):
        if( self.verbose ):
            print( " | INIT HEARTBEAT CHECK", flush=True )

        # Conto i flag che ci sono ora nel db.
        curr_n_flags = self.db.count_flags()
        curr_time = time()

        # Se ho meno di 10 flag non faccio il controllo dell'heartbeat
        if( self.last__flag_count < 10 ):
            self.last__flag_count = curr_n_flags
            self.last__flag_check_time = curr_time
            if( self.verbose ):
                print( " | DONE", flush=True )
            return

        # Sono passati TICK_TIME secondi dall'ultimo check.
        if(curr_time - self.last__flag_check_time > self.TICK_TIME):

            # Se il conteggio dei flag del check effettuato al turno precedente è uguale
            # al conteggio attuale, allora si è piantato l'exploit manager
            if curr_n_flags == self.last__flag_count:
                Notification(
                	title='EXPLOIT MANAGER BLOCCATO!',
                	description='Il flag submitter ha rilevato che sono stati inviati dei flag nei turni precedenti, ma nel turno corrente non ne sono stati aggiunti altri.',
                	icon_path=get_base_folder() + '/InsHack@ti.jpg', # On Windows .ico is required, on Linux - .png
                	duration=self.DELTA_TIME,                              # Duration in seconds
                	urgency=Notification.URGENCY_CRITICAL
                ).send()
                print(' |-- !!!!!!!!!!!!!!!! EXPLOIT MANAGER BLOCCATO !!!!!!!!!!!!!!!!')
                print(' |-- !!!!!!!!!!!!!!!! EXPLOIT MANAGER BLOCCATO !!!!!!!!!!!!!!!!')
                print(' |-- !!!!!!!!!!!!!!!! EXPLOIT MANAGER BLOCCATO !!!!!!!!!!!!!!!!')

            # Aggiorno il conteggio e il datetime
            self.last__flag_check_time = curr_time
            self.last__flag_count = curr_n_flags

        if( self.verbose ):
            print( " | DONE", flush=True )

    def print_banner(self):
        print('')
        print("""  ______ _                _____       _               _ _   _
 |  ____| |              / ____|     | |             (_) | | |
 | |__  | | __ _  __ _  | (___  _   _| |__  _ __ ___  _| |_| |_ ___ _ __
 |  __| | |/ _` |/ _` |  \___ \| | | | '_ \| '_ ` _ \| | __| __/ _ \ '__|
 | |    | | (_| | (_| |  ____) | |_| | |_) | | | | | | | |_| ||  __/ |
 |_|    |_|\__,_|\__, | |_____/ \__,_|_.__/|_| |_| |_|_|\__|\__\___|_|
                  __/ |
                 |___/                                                   """)
        print('')
        print('  EVENT: {}'.format(self.event))
        print('')
        print('-'*80)
        print('')
        print('\tCONFIGURATIONS')
        print('\t[*] Verbose:    {}'.format(self.verbose))
        print('\t[*] Delta time: {} s'.format(self.DELTA_TIME))
        print('\t[*] Tick time:  {} s'.format(self.TICK_TIME))
        print('\t[*] Team token: {}'.format(self.TEAM_TOKEN))
        print('\t[*] Master url: {}'.format(self.master_url))
        print('')
        print('-'*80)
        print('')
