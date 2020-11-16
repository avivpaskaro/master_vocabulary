import queue
import random
import threading

from tonguemaster.DB import MyDB


class Server(threading.Thread):
    """
    TODO: add description here
    """

    def __init__(self, dir_q, result_q, db_file):
        super(Server, self).__init__()
        self.dir_q = dir_q
        self.result_q = result_q
        self.stop_request = threading.Event()
        self.db_file = db_file
        self.db = None

    def run(self):
        if self.db is None:
            self.db = MyDB(self.db_file, 'words')
        self.db.clean_table('words')
        while not self.stop_request.isSet():
            try:
                (job_id, job_type, table, job_params) = self.dir_q.get(True, 0.05)
                if job_type is 'insert_word':
                    '''
                    job_params = [src_lan (str), dst_lan (str)]
                    '''
                    self.db.insert_word(table, job_params)
                elif job_type is 'create_table':
                    '''
                    job_params = []
                    '''
                    self.db.create_table(table)
                elif job_type is 'word_exists':
                    '''
                    job_params = [field, value]
                    return: boolean
                    '''
                    res = self.db.word_exists(table, job_params[0], [job_params[1]])
                    self.result_q.put((self.name, job_id, job_type, res))
                elif job_type is 'update_word':
                    '''
                    job_params = [[columns to update], [rules columns], [new values]]
                    '''
                    self.db.update_word(table, job_params[0], job_params[1], job_params[2])
                elif job_type is 'get_words':
                    '''
                    job_params = [amount (int), [fields]]
                    '''
                    res = self.db.get_words(table, job_params[0], job_params[1])
                    self.result_q.put((self.name, job_id, job_type, res))
                elif job_type is 'clean_table':
                    '''
                    job_params = []
                    '''
                    self.db.clean_table(table)
                elif job_type is 'get_rand':
                    '''
                    job_params = [amount (int), [fields]]
                    '''
                    res = self.db.get_words(table, job_params[0], job_params[1])
                    self.result_q.put((self.name, job_id, job_type, res))
                else:
                    res = "Error"
                    print(job_type)
                    self.result_q.put((self.name, job_id, job_type, res))
            except queue.Empty:
                continue
        # Done: close DB
        self.db.close()

    def join(self, timeout=None):
        self.stop_request.set()
        super(Server, self).join(timeout)

