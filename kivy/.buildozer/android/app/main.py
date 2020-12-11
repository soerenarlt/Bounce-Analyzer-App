import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.app import platform

from plyer import accelerometer
from plyer import spatialorientation
from plyer import gravity

import csv
import os
import numpy as np
import pandas as pd
import numpy.linalg as la

from android.permissions import request_permissions, Permission
from android.storage import primary_external_storage_path



class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid,self).__init__(**kwargs)
        self.cols = 1
        self.recording = False
        self.txt = ""
        self.run=0
        self.store = JsonStore('hello.json')

        self.cwd = os.getcwd()

        with open('check.csv', 'w') as f:
            f.write("time;accx;accy;accz;gravx;gravy;gravz;orient1;orient2;orient3")
            f.write("\n")

        self.inside = GridLayout()
        self.inside.cols = 2

        self.inside.add_widget(Label(text="Accelerator: "))
        self.acc = Label(text="")
        self.inside.add_widget(self.acc)

        self.inside.add_widget(Label(text="Gravity: "))
        self.grav = Label(text="")
        self.inside.add_widget(self.grav)

        self.inside.add_widget(Label(text="Orientation: "))
        self.orient = Label(text="")
        self.inside.add_widget(self.orient)

        self.add_widget(self.inside)

        self.submit = Button(text="Start/Stop recording", font_size=20)
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)

        request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        SD_CARD = primary_external_storage_path()
        os.chdir(os.path.join(SD_CARD, "Kivy"))


    def pressed(self,instance):
        self.recording = not self.recording
        self.iter = 0



        if self.recording:
            self.run += 1
            try:
                accelerometer.enable()
            except:
                self.acc.text = 'whoops'  # error

            try:
                gravity.enable()
            except:
                self.grav.text = 'whoops'  # error

            try:
                spatialorientation.enable_listener()
            except:
                self.orient.text = 'whoops'  # error

            self.submit.text = 'taking data'
            Clock.schedule_interval(self.update, 1.0 / 24)

        else:
            try:
                # t = self.df['time']
                # ax = list(self.df['ax'])
                # ay = list(self.df['ay'])
                # az = list(self.df['az'])
                # a = np.array(list(zip(ax, ay, az)))
                #
                # ax2 = list(self.df['gx'])
                # ay2 = list(self.df['gy'])
                # az2 = list(self.df['gz'])
                # aplusg = np.array(list(zip(ax2, ay2, az2)))
                #
                # accz = []
                # for ind in range(len(self.df)):
                #     diff = aplusg[ind] - a[ind]
                #     vec = diff / (la.norm(diff) + 1e-16)
                #     accz.append(np.dot(vec, a[ind]))
                # accz_mean = np.mean(accz,axis=0)
                # self.submit.text = str(accz_meanc)
                # self.submit.text = str(len(self.df))
                pass
            except:
                self.submit.text = 'no data'


    def update(self,dt):
        if self.recording:
            try:
                acc = accelerometer.acceleration[0:3]
                racc = [round(elem, 2) for elem in acc]
                self.acc.text =str(racc)

            except:
                self.acc.text = "Cannot read accelerometer!"  # error

            try:
                grav = gravity.gravity[0:3]
                rgrav = [round(elem, 2) for elem in grav]
                self.grav.text =str(rgrav)
            except:
                self.txt = "Cannot read accelerometer!"  # error

            try:
                orient = spatialorientation.orientation[0:3]
                rorient = [round(elem, 2) for elem in orient]
                self.orient.text =str(rorient)
            except:
                self.orient.text = "Cannot read orientation!"  # error
            self.iter += 1

            try:
                line=str(self.iter)+";{acc1};{acc2};{acc3};{grav1};{grav2};{grav3};{orient1};{orient2};{orient3}".format(acc1=str(acc[0]),acc2=str(acc[1]),acc3=str(acc[2]),grav1=str(grav[0]),grav2=str(grav[1]),grav3=str(grav[2]),orient1=str(orient[0]),orient2=str(orient[1]),orient3=str(orient[2]))
            except:
                line=";;;;;;;;"

            with open('check.csv', 'a') as f:
                f.write(line)
                f.write("\n")

class BounceApp(App):
    def build(self):
        return MyGrid()
if __name__ == "__main__":
    BounceApp().run()