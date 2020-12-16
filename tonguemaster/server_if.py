import queue
from tonguemaster.sever import Server
from datetime import date, timedelta
from os import path


class ServerIf:

    def __init__(self, db_paths, server_num=1):
        """

        :param server_num: total number of servers
        :param db_paths: path to the db file (excluded)
        """
        self.query_q = queue.Queue()
        self.result_q = queue.Queue()
        self.server_num = server_num
        self.pool = \
            [Server(dir_q=self.query_q, result_q=self.result_q, db_file=path.join(db_paths[i], 'tonguemaster.db'))
             for i in range(server_num)]

    def start_servers(self):
        """
        must run before using the server_if functions
        :return: void
        """
        for thread in self.pool:
            thread.start()

    def are_exist(self, word_list):
        """

        :param word_list: words in src-lan
        :return: list of all non-exists words
        """
        exists = []
        for word in word_list:
            self.__send_job(0, 'word_exists', 'words', ['src_language', word])
            exists.append(self.__get_resp())
        return [word_list[i] for i in range(len(word_list)) if exists[i] is False]

    def insert(self, pairs_list):
        """

        :param pairs_list: every pair (tuple) is (word in src-lan, word in dst-lan) e.g. [(a,a),(b,b)]
        :return: void
        """
        for pair in pairs_list:
            self.__send_job(0, 'insert_word', 'words', list(pair))

    def update_words(self, word_list):
        """

        :param word_list: every tuple contain: (word in src-lan, EZ factor, interval (days), repetitions)
        :return: void
        """
        today = date.today()
        for word in word_list:
            update_col = ['EZ_factor', 'next_date', 'interval', 'repetitions']
            rules_col = ['src_language']
            params = [word[1], str(today + timedelta(days=word[2])), word[2], word[3], word[0]]
            self.__send_job(0, 'update_word', 'words', [update_col, rules_col, params])

    def insert_mp3_fname(self, word_list):
        """

        :param word_list: every tuple contain: (word in src-lan, mp3 file name)
        :return: void
        """

        for word in word_list:
            update_col = ['mp3_file_name']
            rules_col = ['src_language']
            params = [word[1], word[0]]
            self.__send_job(0, 'update_word', 'words', [update_col, rules_col, params])

    def set_word_invalid(self, word_list):
        """

        :param word_list: list of source language words
        :return: void
        """

        for word in word_list:
            update_col = ['valid']
            rules_col = ['src_language']
            params = [0, word]
            self.__send_job(0, 'update_word', 'words', [update_col, rules_col, params])

    def fetch_entries(self):
        """

        :param: null
        :return: list of all dictionary tuples
        """
        self.__send_job(0, 'get_entries', 'words', None)
        return self.__get_resp()

    def fetch_words(self, amount):
        """

        :param amount: number of requested words
        :return: list of tuples when every tuple contain: (word in src-lan, word in dst-lan, EZ factor,
                                                          interval (days), repetitions, mp3 file name)
        """
        self.__send_job(0, 'get_words', 'words', [amount, ['src_language', 'dst_language', 'EZ_factor', 'interval',
                                                           'repetitions', 'mp3_file_name']])
        return self.__get_resp()

    def fetch_dummy(self, amount):
        """

        :param amount: number of requested dummy words
        :return: list of words in dst-lan
        """
        self.__send_job(0, 'get_rand', 'words', [amount, ['dst_language']])
        return [word[0] for word in self.__get_resp()]

    def __send_job(self, job_id, job_type, table, params):
        self.query_q.put((job_id, job_type, table, params))

    def __get_resp(self):
        return self.result_q.get()[3]

    def stop_servers(self):
        for thread in self.pool:
            thread.join()
