import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore

class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid,self).__init__(**kwargs)
        self.store = JsonStore('hello.json')
        self.recording = False
        self.iter = 0

        self.submit = Button(text="Start/Stop recording", font_size=20)
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)


    def pressed(self,instance):
        self.recording = not self.recording

        if self.recording:
            Clock.schedule_interval(self.update, 1.0 / 24)
        else:
            pass

    def update(self,dt):
        if self.recording:
            self.store.put(self.iter,col1=1,col2=2,col3=3)
        self.iter +=1

class DataApp(App):
    def build(self):
        return MyGrid()
if __name__ == "__main__":
    DataApp().run()