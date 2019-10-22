import kivy
from functools import partial
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

kivy.require('1.11.1')


def init_window(height, width):
    Window.clearcolor = (1, 1, 1, 1)
    Window.size = (height, width)


def switch_screen(self, screen_name, *args):
    self.manager.current = screen_name


class LogoImg(Image):

    def __init__(self, **kwargs):
        super(LogoImg, self).__init__(**kwargs)

        # param for the image
        self.source = 'PLScare/assets/images/logo_PLScare.png'
        self.size_hint = (None, None)
        self.size_hint = 0.8, 0.8
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.7}


class SolutionImg(Image):

    def __init__(self, path, x, y, **kwargs):
        super(SolutionImg, self).__init__(**kwargs)

        # param for the image
        self.source = path
        self.size_hint = (None, None)
        self.size_hint = 0.8, 0.8
        self.pos_hint = {'center_x': x, 'center_y': y}


class AskLabel(Label):

    def __init__(self, **kwargs):
        super(AskLabel, self).__init__(**kwargs)

        # param for the label
        self.text = 'La victime présente-t-elle des signes de saignements ?'
        self.color = 1, 0, 0, 1
        self.font_name = 'PLScare/assets/fonts/OpenSans-Bold.ttf'
        self.font_size = 40
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.8}


class CustomBtn(Button):

    def __init__(self, x, y, text, size, **kwargs):
        super(CustomBtn, self).__init__(**kwargs)

        # param for the button
        self.text = text
        self.size_hint = (None, None)
        self.pos_hint = {'center_x': x, 'center_y': y}
        self.font_name = 'PLScare/assets/fonts/OpenSans-Bold.ttf'
        self.font_size = size
        self.color = 1, 0, 0, 1
        self.padding = (30, 10)
        self.background_normal = ''
        self.background_down = 'PLScare/assets/images/grey.png'


class FirstScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

        # declaration des elements
        btn_hub = CustomBtn(0.5, 0.3, 'Enregistrer', 50)
        img_logo = LogoImg()

        # event on button
        btn_hub.bind(on_press=partial(switch_screen, self, '_second_screen_'))

        # add element in screen
        self.add_widget(btn_hub)
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

        # declaration des elements
        sol_img = SolutionImg('PLScare/assets/situations/arret/arretcardiaque1_medium-187.png', 0.1, 0.5)

        # add element in screen
        self.add_widget(sol_img)


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
