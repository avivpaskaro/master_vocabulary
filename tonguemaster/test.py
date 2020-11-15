import threading
import time
import random
# Constants
ADD = '1'
MENU = '2'


class Test(threading.Thread):
    def __init__(self, words_lst):
        """
        Class constructor

        :param words_lst: get word list from study thread, this list is the test list
        """
        threading.Thread.__init__(self)
        self.words_lst = words_lst
        print('\nWelcome to test session!')

    @staticmethod
    def rand_answers(right_answer, answers_lst):
        """
        for each word we random 3 wrongs answers and shuffle
        them with the right answer. those are the answers that the
        user will need to choose from.

        :param answers_lst: list of all the answer of the entire test session
        :param right_answer: the right answer
        :return: shuffle list with the right answer
        """
        answers_without_right_answer = [x for x in answers_lst if x not in right_answer]
        rand_answers_lst = random.sample(range(0, len(answers_without_right_answer)), 3)  # 3 is optional
        answers = [answers_without_right_answer[i] for i in rand_answers_lst]
        answers.append(right_answer)
        random.shuffle(answers)
        return answers

    def run(self):
        """
        run test session for each word will show 4 different
        answer that the user will need to choose from.

        :return: none
        """
        translations = [x[1] for x in self.words_lst]
        for word_tuple in self.words_lst:
            answers = self.rand_answers(word_tuple[1], translations)
            print(f'{word_tuple[0]} - answers: {answers}')
            time.sleep(5)
