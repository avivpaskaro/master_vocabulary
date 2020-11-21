import threading
from tonguemaster.server_if import ServerIf
import random
import time
import supermemo2

# Constants
ADD = '1'
MENU = '2'
FALSE_ANS_NUM = 4
PERFECT_TIME = 5
GOOD_TIME = 10


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
    def calc_q(time_elapsed, life, is_idk):
        if is_idk:
            q = 0
        elif life == 3:
            if time_elapsed < PERFECT_TIME:
                q = 5
            elif time_elapsed < GOOD_TIME:
                q = 4
            else:
                q = 3
        else:
            q = life
        return q

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
        rand_sample = random.sample(range(len(answers_lst)), FALSE_ANS_NUM)
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
        for word_tuple in self.words_lst:
            word, translate, easy_factor, interval, repetitions = word_tuple
            print(f'\nword tuple: {word_tuple}')
            answers = self.rand_answers(translate,
                                        list(set(dummy_answers.copy())))
            start_time = time.time()
            chose_idk_flag = False
            life = 3
            time_elapsed = 0
            while True:
                idx = 1
                print(f'\n{word}:')
                for answer in answers:
                    print(f'{idx}. {answer}')
                    idx += 1
                print(f'{idx}. I don\'t know :(')
                user_choice = input('your answer: ')
                if not user_choice or int(user_choice) not in range(1, FALSE_ANS_NUM + 3):
                    print('you chose not valid answer')
                else:
                    user_choice = int(user_choice)
                    if user_choice == FALSE_ANS_NUM + 2:  # user chose IDK
                        print(f'Right answer is: {translate}')
                        chose_idk_flag = True
                        break
                    elif answers[user_choice - 1] == translate:
                        print('you were right!')
                        time_elapsed = time.time() - start_time
                        break
                    else:
                        print('you were wrong!')
                        answers.remove(answers[user_choice - 1])
                        life -= 1
                        if not life:
                            print(f'\nRight answer is: {translate}')
                            break
            q = self.calc_q(time_elapsed=time_elapsed, life=life, is_idk=chose_idk_flag)
            sm2 = supermemo2.SMTwo(quality=q, interval=interval, repetitions=repetitions, easiness=easy_factor,
                                   first_visit=False if repetitions != 0 else True)
            result = sm2.json()
            ServerIf.update_words(self.server, [(word, result['new_easiness'], result['new_interval'],
                                                 result['new_repetitions'])])
