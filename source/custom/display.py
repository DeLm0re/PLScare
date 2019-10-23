import kivy
import os
from functools import partial
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

kivy.require('1.11.1')

# -------------------------------------------------------------------------------------------------------------
# -------------------------------------    FUNCTION DEFINITION    ---------------------------------------------
# -------------------------------------------------------------------------------------------------------------


def init_window(height, width):
    Window.clearcolor = (1, 1, 1, 1)
    Window.size = (height, width)


def switch_screen(self, screen_name, *args):
    self.manager.current = screen_name


def setup_solution(screen, situation_name):
    add_solutions_icons(screen, situation_name)
    add_solutions_labels(screen, situation_name)


def add_solutions_icons(screen, situation_name):
    # declaration de la liste des images
    path = 'custom/assets/icons/' + situation_name
    list_sol = sorted(os.listdir(path))
    total_sol = len(list_sol)

    # pour toutes les images de solution
    for index_sol in range(0, total_sol):
        # add element in screen
        sol_img = SolutionImg(path + '/' + list_sol[index_sol], 0.1, index_sol / (total_sol + 1) + 0.1)
        screen.add_widget(sol_img)


def add_solutions_labels(screen, situation_name):
    # declaration du fichier de solution
    file = open('custom/assets/solutions/' + situation_name + '.txt', 'r')
    lines = file.readlines()
    nbr_lines = len(lines)

    # pour chaque ligne du fichier
    for index_sol in range(0, nbr_lines):
        sol_label = SolutionLabel(lines[index_sol], 0.6, index_sol / (nbr_lines + 1) + 0.1)
        screen.add_widget(sol_label)


# -------------------------------------------------------------------------------------------------------------
# ---------------------------------------    CLASS DEFINITION    ----------------------------------------------
# -------------------------------------------------------------------------------------------------------------


class LogoImg(Image):

    def __init__(self, **kwargs):
        super(LogoImg, self).__init__(**kwargs)

        # param for the image
        self.source = 'custom/assets/images/logo_PLScare.png'
        self.size_hint = (None, None)
        self.size_hint = 0.8, 0.8
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.75}


class SolutionImg(Image):

    def __init__(self, path, x, y, **kwargs):
        super(SolutionImg, self).__init__(**kwargs)

        # param for the image
        self.source = path
        self.pos_hint = {'center_x': x, 'center_y': y}


class SolutionLabel(Label):

    def __init__(self, text, x, y, **kwargs):
        super(SolutionLabel, self).__init__(**kwargs)

        # param for the label
        self.text = text
        self.color = 0, 0, 0, 1
        self.font_name = 'custom/assets/fonts/OpenSans-Bold.ttf'
        self.font_size = 14
        self.pos_hint = {'center_x': x, 'center_y': y}


class AskLabel(Label):

    def __init__(self, **kwargs):
        super(AskLabel, self).__init__(**kwargs)

        # param for the label
        self.text = 'La victime présente-t-elle des signes de saignements ?'
        self.color = 1, 0, 0, 1
        self.font_name = 'custom/assets/fonts/OpenSans-Bold.ttf'
        self.font_size = 40
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.8}


class CustomBtn(Button):

    def __init__(self, x, y, text, size, **kwargs):
        super(CustomBtn, self).__init__(**kwargs)

        # param for the button
        self.text = text
        self.size_hint = (None, None)
        self.pos_hint = {'center_x': x, 'center_y': y}
        self.font_name = 'custom/assets/fonts/OpenSans-Bold.ttf'
        self.font_size = size
        self.color = 1, 0, 0, 1
        self.padding = (30, 10)
        self.background_normal = ''
        self.background_down = 'custom/assets/images/grey.png'


class FirstScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

        # declaration des elements
        record_btn = CustomBtn(0.5, 0.4, 'Enregistrer', 45)
        video_btn = CustomBtn(0.5, 0.15, 'Video', 45)

        img_logo = LogoImg()

        # event on button
        record_btn.bind(on_press=partial(switch_screen, self, '_second_screen_'))
        video_btn.bind(on_press=partial(switch_screen, self, '_second_screen_'))

        # add element in screen
        self.add_widget(record_btn)
        self.add_widget(video_btn)
        self.add_widget(img_logo)


class SecondScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

        # declaration des elements
        ask_label = AskLabel()
        yes_btn = CustomBtn(0.5, 0.5, 'Oui', 40)
        no_btn = CustomBtn(0.5, 0.2, 'Non', 40)

        # event on button
        yes_btn.bind(on_press=partial(switch_screen, self, '_third_screen_'))
        no_btn.bind(on_press=partial(switch_screen, self, '_third_screen_'))

        # add element in screen
        self.add_widget(ask_label)
        self.add_widget(yes_btn)
        self.add_widget(no_btn)


class ThirdScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

        # example of a situation
        setup_solution(self, 'Arret_cardiaque')


class PlscareApp(App):

    def build(self):
        # init the screen manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(FirstScreen(name='_first_screen_'))
        screen_manager.add_widget(SecondScreen(name='_second_screen_'))
        screen_manager.add_widget(ThirdScreen(name='_third_screen_'))
        return screen_manager


def run_app():
    # init the screen size
    init_window(600, 600)

    # run the app
    PlscareApp().run()
