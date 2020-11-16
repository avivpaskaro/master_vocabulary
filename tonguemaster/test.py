import threading
from tonguemaster.server_if import ServerIf
import random
# Constants
ADD = '1'
MENU = '2'


class Test(threading.Thread):
    def __init__(self, words_lst, server):
        """
        Class constructor

        :param words_lst: get word list from study thread, this list is the test list
        """
        threading.Thread.__init__(self)
        self.words_lst = words_lst
        self.server = server
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
        if right_answer in answers_lst:
            answers_lst.remove(right_answer)
        rand_sample = random.sample(range(len(answers_lst)), 3)  # 3 is optional
        answers = [answers_lst[i] for i in rand_sample]
        answers.append(right_answer)
        random.shuffle(answers)
        return answers

    def run(self):
        """
        run test session for each word will show 4 different
        answer that the user will need to choose from.

        :return: none
        """
        dummy_answers = ServerIf.fetch_dummy(self.server, 50)
        words = [x[0] for x in self.words_lst]
        translations = [x[1] for x in self.words_lst]
        for i in range(len(words)):
            print(f'\n{words[i]}:')
            answers = self.rand_answers(translations[i], list(set(dummy_answers.copy())))
            for j in range(len(answers)):
                print(f'{j+1}. {answers[j]}')
            while True:
                user_choice = input('your answer: ')
                if not user_choice or int(user_choice) not in range(1, 5):
                    print('you chose not valid answer')
                    continue
                else:
                    break
            if answers[int(user_choice)-1] == translations[i]:
                print('you were right!')
            else:
                print('you were wrong!')
