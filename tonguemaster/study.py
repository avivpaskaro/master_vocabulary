import time

from tonguemaster.server_if import ServerIf
from tonguemaster.test import *


class Study(threading.Thread):
    # Global
    FIVE = '1'
    TEN = '2'
    FIFTEEN = '3'

    def __init__(self, dictionary, server):
        """
        Class constructor

        :param dictionary: The global dictionary, will be used to fetch words from
        """
        threading.Thread.__init__(self)
        self.dictionary = dictionary
        self.server = server

    def run(self):
        """
        Run infinite loop to get from use the proper number of words to study.
        after use has chosen quantity, he will study them one by one.
        lastly he will be testing on them.

        :return: none
        """
        while True:
            words_quantity = input(f'\n{{Study}} Welcome to study session!\n' +
                                   '{{Study}} Please choose how many words do you want to study:\n' +
                                   '{{Study}} 1. 5 Words\n' +
                                   '{{Study}} 2. 10 Words\n' +
                                   '{{Study}} 3. 15 Words\n')
            if words_quantity == self.FIVE:
                words_quantity = 5
                break
            elif words_quantity == self.TEN:
                words_quantity = 10
                break
            elif words_quantity == self.FIFTEEN:
                words_quantity = 15
                break
            else:
                print('Chose wrong, try again!')

        # study session
        words_lst = ServerIf.fetch_words(self.server, words_quantity)
        for words_tuple in words_lst:
            (words, answer) = words_tuple
            print(f'{words}')
            time.sleep(0.1)
            print(f'{answer}\n')
            time.sleep(0.1)

        # invoke test thread
        t = Test(words_lst)
        t.start()
        t.join()
