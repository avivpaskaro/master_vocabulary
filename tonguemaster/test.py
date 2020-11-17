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
        rand_sample = random.sample(range(len(answers_lst)), 5)  # 3 is optional
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
        score = 0
        for pair in self.words_lst:
            life = 3
            word, translate, EF = pair
            print(f'\n{word}:')
            answers = self.rand_answers(translate,
                                        list(set(dummy_answers.copy())))
            while True:
                idx = 1
                for answer in answers:
                    print(f'{idx}. {answer}')
                    idx += 1
                user_choice = input('your answer: ')
                if not user_choice or int(user_choice) not in range(1, 7):
                    print('you chose not valid answer')
                else:
                    user_choice = int(user_choice) - 1
                    if answers[user_choice] == translate:
                        print('you were right!')
                        if life is 3:
                            score += 30
                        elif life is 2:
                            score += 20
                        elif life is 1:
                            score += 10
                        break
                    else:
                        print('you were wrong!')
                        print(f'\n{word}:')
                        answers.remove(answers[user_choice])
                        life -= 1
        print(f'\nYour score is: {score}')

