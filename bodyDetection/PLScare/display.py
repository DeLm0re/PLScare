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

    def __init__(self, **kwargs):
        super(SolutionImg, self).__init__(**kwargs)

        # param for the image
        self.source = 'PLScare/assets/situations/arret/arretcardiaque1_medium-187.png'
        self.size_hint = (None, None)
        self.size_hint = 0.8, 0.8
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.7}


class HubBtn(Button):

    def __init__(self, **kwargs):
        super(HubBtn, self).__init__(**kwargs)

        # param for the button
        self.text = 'Start recording'
        self.size_hint = (None, None)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.3}
        self.font_name = 'PLScare/assets/fonts/OpenSans-Bold.ttf'
        self.font_size = 50
        self.color = 1, 0, 0, 1
        self.padding = (30, 10)
        self.background_normal = ''
        self.background_down = 'PLScare/assets/images/grey.png'


class AskLabel(Label):

    def __init__(self, **kwargs):
        super(AskLabel, self).__init__(**kwargs)

        # param for the label
        self.text = 'La victime présente elle des signes de saignements ?'
        self.color = 1, 0, 0, 1
        self.font_name = 'PLScare/assets/fonts/OpenSans-Bold.ttf'
        self.font_size = 40
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.8}


class YesBtn(Button):

    def __init__(self, **kwargs):
        super(YesBtn, self).__init__(**kwargs)

        # param for the button
        self.text = 'Oui'
        self.size_hint = (None, None)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.font_name = 'PLScare/assets/fonts/OpenSans-Bold.ttf'
        self.font_size = 40
        self.color = 1, 0, 0, 1
        self.padding = (30, 10)
        self.background_normal = ''
        self.background_down = 'PLScare/assets/images/grey.png'


class NoBtn(Button):

    def __init__(self, **kwargs):
        super(NoBtn, self).__init__(**kwargs)

        # param for the button
        self.text = 'Non'
        self.size_hint = (None, None)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.2}
        self.font_name = 'PLScare/assets/fonts/OpenSans-Bold.ttf'
        self.font_size = 40
        self.color = 1, 0, 0, 1
        self.padding = (30, 10)
        self.background_normal = ''
        self.background_down = 'PLScare/assets/images/grey.png'


class FirstScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

        # declaration des elements
        btn_hub = HubBtn()
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
        yes_btn = YesBtn()
        no_btn = NoBtn()

        # add element in screen
        self.add_widget(ask_label)
        self.add_widget(yes_btn)
        self.add_widget(no_btn)


class ThirdScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)


class PlscareApp(App):

    def build(self):
        # init the screen size
        init_window(600, 600)

        # init the screen manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(FirstScreen(name='_first_screen_'))
        screen_manager.add_widget(SecondScreen(name='_second_screen_'))
        screen_manager.add_widget(ThirdScreen(name='_third_screen_'))
        return screen_manager


def run_app():
    PlscareApp().run()
