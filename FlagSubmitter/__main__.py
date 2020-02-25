from sys import argv
from .flag_submitter import FlagSubmitter
from signal import signal, SIGINT

def signal_handler(sig, frame):
    print('')
    print('Rilevato Ctrl+C! Esco...')
    print('')
    exit(0)

signal(SIGINT, signal_handler)


def get_base_folder():
    from os.path import dirname, abspath
    return abspath( dirname( abspath(__file__) ) + '/../' )


if __name__ == '__main__':
    flag_submitter = FlagSubmitter(argv)

    # Controlla per nuovi flag da inviare ogni 6 secondi.
    flag_submitter.DELTA_TIME = 5

    # Durata del turno in secondi
    flag_submitter.TICK_TIME = 12

    # Imposta la modalita
    flag_submitter.verbose = True

    flag_submitter.print_banner()
    flag_submitter.run()
