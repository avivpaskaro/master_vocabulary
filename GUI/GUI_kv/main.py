import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.checkbox import CheckBox
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from time import sleep, time
from kivy.uix.popup import Popup

kv = Builder.load_file("myGrid.kv")

red = [1, 0, 0, 1]
green = [0, 1, 0, 1]
blue = [0, 0, 1, 1]
purple = [1, 0, 1, 1]
white = [1, 1, 1, 1]

g_word_list = [['Aviv', 'Spring', 2], ['Eldad', 'Wiener', 1], ['holly', 'sheep', 3]]
g_dummy_word_list = ['a', 'b', 'c']


class MyMainApp(Screen):
    pass


class MyLearnScreenDone(Screen):
    pass


class MyLearnScreenOpen(Screen):
    pass


class MyLearnScreen(Screen):
    b1 = ObjectProperty(None)
    b2 = ObjectProperty(None)
    b3 = ObjectProperty(None)
    kv_state = ObjectProperty(None)
    counter = ObjectProperty(None)
    src_word = ObjectProperty(None)
    dst_word = ObjectProperty(None)
    passed_arg = "old_val"
    word_idx = 0
    word_state_idx = 2
    word_src_idx = 0
    word_dst_idx = 1
    word_list = g_word_list
    state = word_list[word_idx][word_state_idx]
    colors = [red, green, blue, purple]
    max_num_words = 15
    words_num = max_num_words if max_num_words < len(word_list) else len(word_list)

    def star_btn(self, idx):
        if self.word_idx < self.words_num:
            self.state = idx if idx < 4 else self.state
            self.word_list[self.word_idx][self.word_state_idx] = self.state
            self.counter.text = str(int(self.counter.text) + 1)
            self.b1.background_normal = '../star_y.png' if self.state >= 1 else '../star_g.png'
            self.b1.background_down = '../star_y_p.png' if self.state >= 1 else '../star_g_p.png'
            self.b2.background_normal = '../star_y.png' if self.state >= 2 else '../star_g.png'
            self.b2.background_down = '../star_y_p.png' if self.state >= 2 else '../star_g_p.png'
            self.b3.background_normal = '../star_y.png' if self.state >= 3 else '../star_g.png'
            self.b3.background_down = '../star_y_p.png' if self.state >= 3 else '../star_g_p.png'

    def nxt_btn(self, step):
        self.word_idx += step
        if self.word_idx >= self.words_num:
            self.word_idx = 0
            self.kv_state.text = 'Done'
            sm.transition.direction = 'left'
            sm.current = 'learn_done'
            # sm.switch_to(screen=sm.screens[2], direction='right')
        elif self.word_idx < 0:
            self.word_idx = 0
        else:
            self.star_btn(self.word_list[self.word_idx][self.word_state_idx])
            self.src_word.text = self.word_list[self.word_idx][self.word_src_idx]
            self.dst_word.text = self.word_list[self.word_idx][self.word_dst_idx]

    def on_pre_enter(self):
        self.reset_screen()

    def reset_screen(self):
        self.word_idx = 0
        self.words_num = self.max_num_words if self.max_num_words < len(self.word_list) else len(self.word_list)
        self.nxt_btn(0)


class MyTestScreen(Screen):
    src_word = ObjectProperty(None)
    ans_1 = ObjectProperty(None)
    ans_2 = ObjectProperty(None)
    ans_3 = ObjectProperty(None)
    ans_4 = ObjectProperty(None)

    ans_lst = []

    word_idx = 0
    word_src_idx = 0
    word_dst_idx = 1
    word_list = g_word_list
    dummy_words = g_dummy_word_list
    timer = 0
    popupWindow = None

    def btn_click(self, ans_idx):
        ans = self.ans_lst[ans_idx - 1]
        dst_ans = ans.text
        if self.word_list[self.word_idx][self.word_dst_idx] == dst_ans:
            elapse_time = time() - self.timer
            print(elapse_time)
            self.word_idx += 1
            self.show_popup()
            self.new_word()
        else:
            ans.disabled = True

    def new_word(self):
        self.timer = time()
        if self.word_idx >= len(self.word_list):
            self.word_idx = 0
            sm.transition.direction = 'left'
            sm.current = 'test_done'
        else:
            for i, ans in enumerate(self.ans_lst):
                ans.disabled = False
                ans.state = 'normal'
                if i == 0:
                    ans.text = self.word_list[self.word_idx][self.word_dst_idx]
                else:
                    ans.text = self.dummy_words[i - 1]
            self.src_word.text = self.word_list[self.word_idx][self.word_src_idx]

    def on_pre_enter(self):
        self.reset_screen()

    def reset_screen(self):
        self.word_idx = 0
        self.ans_lst = [self.ans_1, self.ans_2, self.ans_3, self.ans_4]
        self.new_word()

    def show_popup(self):
        self.popupWindow = Popup(title="Test message", content=Label(text="You were right!!", font_size=24),
                                 size_hint=(None, None), size=(300, 200))
        self.popupWindow.bind(on_dismiss=self.popup_callback)
        # Create the popup window
        self.popupWindow.open()  # show the popup

    def popup_callback(self, instance):
        self.timer = time()


class MyTestScreenDone(Screen):
    pass


sm = ScreenManager()
sm.add_widget(MyMainApp(name='main'))
sm.add_widget(MyLearnScreen(name='learn'))
sm.add_widget(MyLearnScreenDone(name='learn_done'))
sm.add_widget(MyTestScreen(name='test'))
sm.add_widget(MyTestScreenDone(name='test_done'))
sm.add_widget(MyLearnScreenOpen(name='learn_open'))

'''
class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)

        self.cols = 1

        self.first_layout = GridLayout()
        self.first_layout.cols = 2
        self.first_layout.add_widget(Label(text="Name: "))
        self.name = TextInput(multiline=False)
        self.first_layout.add_widget(self.name)

        self.first_layout.add_widget(Label(text="last Name: "))
        self.last_name = TextInput(multiline=False)
        self.first_layout.add_widget(self.last_name)

        self.first_layout.add_widget(Label(text="Email: "))
        self.email = TextInput(multiline=False)
        self.first_layout.add_widget(self.email)

        self.add_widget(self.first_layout)

        self.submit = Button(text="submit", font_size=40)
        self.submit.bind(on_press=self.on_click)
        self.add_widget(self.submit)

    def on_click(self, instance):
        name = self.name.text
        last = self.last_name.text
        email = self.email.text

        print(f"name: {name}, last: {last}, email: {email}")
        self.name.text = ""
        self.last_name.text = ""
        self.email.text = ""
'''


class MyApp(App):
    def build(self):
        return sm


def main():
    MyApp().run()


if __name__ == '__main__':
    main()
