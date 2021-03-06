import time
import uuid
from queue import Queue
import os
from googletrans import Translator
from gtts import gTTS
import threading
from tonguemaster.server_if import ServerIf

EN_DOWNLOAD_MP3 = False


class DownloadMP3(threading.Thread):
    def __init__(self, word, lng, download_q):
        """
        Class constructor

        :param word: The words in foreign language
        :param lng: The foreign language
        :param download_q: Queue to store the threads success marks
        """
        threading.Thread.__init__(self)
        self.word = word
        self.lng = lng
        self.download_q = download_q
        # Create vocals directory to store vocals per language inside
        if not os.path.isdir(f'../vocals/'):
            os.mkdir(f'../vocals/')

    def run(self):
        """
        downloading to mp3 vocal of a given words in a given language

        :return: none (store values in queue)
        """
        # Create language directory to store vocals
        if not os.path.isdir(f'../vocals/{self.lng}'):
            os.mkdir(f'../vocals/{self.lng}')
        try:
            fname = self.lng + uuid.uuid4().hex
            if EN_DOWNLOAD_MP3:
                tts = gTTS(self.word, lang=self.lng)
                tts.save(f'../vocals/{self.lng}/{fname}.mp3')
            self.download_q.put((self.word, fname))
        except Exception as exp:
            pass


class Translate(threading.Thread):
    def __init__(self, word, src_lng, dst_lng, translate_q):
        """
        Class constructor

        :param word: The words in foreign language
        :param src_lng: The foreign language
        :param dst_lng: The destination language
        :param translate_q: Queue to store the threads translations
        """
        threading.Thread.__init__(self)
        self.word = word
        self.src_lng = src_lng
        self.dst_lng = dst_lng
        self.translate_q = translate_q

    def run(self):
        """
        Trying to translate from google a given word
        from source language to destination language.

        :return: none (store values in queue)
        """
        translator = Translator()
        try:
            translation = translator.translate(self.word, src=self.src_lng, dest=self.dst_lng).text
            self.translate_q.put([self.word, translation])
        except Exception as exp:
            pass


class AddWord(threading.Thread):
    # Global variables
    ADD = '1'
    MENU = '2'
    RESULTS_QUEUE = Queue()

    def __init__(self, dictionary, event, server):
        """
        Class constructor

        :param dictionary: pointer of the dictionary database
        :param event: this event is from the main thread,
        the main waits until we set the event on and then he proceed in action
        """
        threading.Thread.__init__(self)
        self.name = 'Add Word'
        self.dictionary = dictionary
        self.event = event
        self.server = server
        self.daemon = True
        print(f'\n{{{self.name}}} Welcome to add word!')

    @staticmethod
    def read_file(file_path):
        """
        Read a file, split content into lines to strip white
        spaces and none string values.


        :param file_path: file path relative to script / file full path
        :return: list of words from file
        """
        with open(file_path, 'r') as f:
            line_lst = f.read().splitlines()
        line_lst = list(map(lambda x: x.strip(), line_lst))
        return list(filter(None, line_lst))

    def run(self):
        """
        Run function of the add words class. It responsible of reading
        words from file and check whom exist in the dictionary. the
        new words are translated and stored in the dictionary.
        It also download the mp3 vocal for that voice and store
        it in directory under ../vocals/"language"/

        :return: none
        """

        self.event.set()

        # todo - commented until the lib will be fixed
        ''' 
            file_path = input(f'{{{self.name}}} Please enter your file name:\n{{{self.name}}} ')
            words_lst = self.read_file(file_path)
            
    
            # word translate threads
            it = 0
            new_words = []
        
            while True:  # Until succeed
            mismatches = ServerIf.are_exist(self.server, words_lst)  # the words that are still not in dictionary
            if it == 0:
                new_words = mismatches  # save the first iteration mismatch list to future use in mp3 threads
            if not mismatches:
                break  # each iteration mismatch list is shrinking, and when its empty we finish job
            threads = []
            for word in mismatches:  # Create threads workers
                t = Translate(word=word, src_lng='it', dst_lng='en', translate_q=self.RESULTS_QUEUE)
                threads.append(t)
                t.start()
            for t in threads:  # wait for threads to finish
                t.join()
            while not self.RESULTS_QUEUE.empty():  # insert results to dictionary
                ServerIf.insert(self.server, [self.RESULTS_QUEUE.get()])
            it += 1
        '''
        tmp_words_list = [('comprare', 'buy'),
                          ('able potere', 'can/be'),
                          ('cancellare', 'cancel'),
                          ('cambiare', 'change'),
                          ('pulire', 'clean'),
                          ('pettinare', 'comb'),
                          ('lamentarsi', 'complain'),
                          ('tossire', 'cough'),
                          ('contare', 'count'),
                          ('tagliare', 'cut'),
                          ('ballare', 'dance'),
                          ('disegnare', 'draw'),
                          ('bere', 'drink'),
                          ('guidare', 'drive'),
                          ('mangiare', 'eat'),
                          ('spiegare', 'explain'),
                          ('cadere', 'fall'),
                          ('rempire', 'fill'),
                          ('trovare', 'find'),
                          ('finire', 'finish')]

        ServerIf.insert(self.server, tmp_words_list)  # todo changes back to original word list

        # mp3 vocals download threads
        download_fail = [x[0] for x in tmp_words_list]  # todo changes back to original word list
        download_successful = []
        while True:  # Until succeed
            if not download_fail:
                ServerIf.insert_mp3_fname(self.server, download_successful)
                break  # Each iteration mismatch list shrinks and when its empty we finish job
            threads = []
            for word in download_fail:  # Create threads workers
                t = DownloadMP3(word=word, lng='it', download_q=self.RESULTS_QUEUE)
                threads.append(t)
                t.start()
            for t in threads:  # wait for threads to finish
                t.join()
            while not self.RESULTS_QUEUE.empty():  # insert results to dictionary
                download_successful.append(self.RESULTS_QUEUE.get())
            # unsuccessfully downloaded
            download_fail = [x for x in download_fail if x not in [y[0] for y in download_successful]]
        time.sleep(2)
