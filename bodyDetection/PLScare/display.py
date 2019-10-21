import kivy
from functools import partial
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

kivy.require('1.11.1')


def init_window(height, width):
    Window.clearcolor = (1, 1, 1, 1)
    Window.size = (height, width)


def run_app():
    PlscareApp().run()


class PlscareApp(App):

    def build(self):
        return PLScareManager()


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


class FirstScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

        # init the screen size
        init_window(600, 600)

        # declaration des elements
        btn_hub = HubBtn()
        img_logo = LogoImg()

        # event on button
        btn_hub.bind(on_press=partial(switch_screen, '_second_screen_'))

        # add element in screen
        self.add_widget(btn_hub)
        self.add_widget(img_logo)


class SecondScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)


class ThirdScreen(Screen):

    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)


class PLScareManager(ScreenManager):

    def __init__(self, **kwargs):
        super(PLScareManager, self).__init__(**kwargs)
        switch_screen('_first_screen_')


def switch_screen(screen_name, *args):
    print(screen_name)
    PLScareManager.current = screen_name
