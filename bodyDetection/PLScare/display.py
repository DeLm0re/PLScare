import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.window import Window

kivy.require('1.11.1')


def init_window(height, width):
    Window.clearcolor = (1, 1, 1, 1)
    Window.size = (height, width)


def run_app():
    PlscareApp().run()


class PlscareApp(App):

    def build(self):
        return PlscareLayout()


class LogoImg(Image):

    def __init__(self, **kwargs):
        super(LogoImg, self).__init__(**kwargs)

        # param for the image
        self.source = 'PLScare/assets/images/logo_PLScare.png'
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


class PlscareLayout(FloatLayout):

    def __init__(self, **kwargs):
        super(PlscareLayout, self).__init__(**kwargs)

        # init the window
        init_window(600, 600)

        # declaration des hub elements
        btn_hub = HubBtn()
        img_logo = LogoImg()

        # event on hub button
        btn_hub.bind(on_press=self.checkout)

        # add element in layout
        self.add_widget(btn_hub)
        self.add_widget(img_logo)

    def checkout(self, value):
        self.clear_widgets()
