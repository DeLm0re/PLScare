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


def on_event(obj):
    print('Typical event from', obj)


def on_property(obj, value):
    print('Typical property change from', obj, 'to', value)


def on_anything(*args, **kwargs):
    print('The flexible function has *args of', str(args),
          'and **kwargs of', str(kwargs))


class ImgLogo(Image):
    pass


class BtnHub(Button):
    pass


class DemoBox(FloatLayout):

    def __init__(self, **kwargs):
        super(DemoBox, self).__init__(**kwargs)

        # init the window
        init_window(600, 600)

        # declaration des hub elements
        btn_hub = BtnHub()
        img_logo = ImgLogo()

        # event on hub button
        btn_hub.bind(on_press=on_event)

        # add element in layout
        # check .kv file
        self.add_widget(btn_hub)
        self.add_widget(img_logo)


class DemoApp(App):
    def build(self):
        return DemoBox()


if __name__ == '__main__':
    DemoApp().run()
