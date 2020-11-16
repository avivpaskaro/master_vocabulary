import os
from tonguemaster.add_word import AddWord
from tonguemaster.study import Study
import numpy as np
from threading import Event
from tonguemaster.server_if import ServerIf


def main():
    # Constants
    ADD = '1'
    STUDY = '2'
    DICT = '3'
    EXIT = '4'
    DICTIONARY = []

    # Create server
    if not os.path.isdir('../db'):
        os.mkdir('../db')
    server_if = ServerIf(db_paths=[r'../db'])
    server_if.start_servers()

    while True:
        """
        Running infinite loop until user choose the EXIT option.
        Otherwise the user has to choose the next action -
        1. Add words
        2. Study
        3. Watch his dictionary
        
        """
        next_action = input('\n{Menu} Welcome to Tongue-Master!\n' +
                            '{Menu} Please enter your next action:\n' +
                            '{Menu} 1. Add Words\n' +
                            '{Menu} 2. Study\n' +
                            '{Menu} 3. Show Dict\n' +
                            '{Menu} 4. Exit\n{Menu} ')

        if next_action == ADD:
            """ 
            The main thread will sleep on event 
            until AddWord will signal him to wake up
            """
            event = Event()
            t = AddWord(dictionary=DICTIONARY, event=event, server=server_if)
            t.start()
            event.wait()
        elif next_action == STUDY:
            t = Study(dictionary=DICTIONARY, server=server_if)
            t.start()
            t.join()
        elif next_action == DICT:
            print(np.array(DICTIONARY))
        elif next_action == EXIT:
            print('{Menu} Bye!')
            server_if.stop_servers()
            exit(0)
        else:
            print('{Menu} You chose wrong action')


if __name__ == '__main__':
    main()
