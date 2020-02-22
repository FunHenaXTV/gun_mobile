from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import (Color, Ellipse, Line)
from kivy.clock import Clock
from kivy.config import Config
from random import random, randint
from time import sleep


Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '800')



class PainterWidget(Widget):
    
    def my_init(self):
        with self.canvas:
            self.length = 100
            self.bullet_exist = 0
            self.targets()
            self.gun()

    def gun(self):
        with self.canvas:
            Color(0, 1, 0, 1)
            self.gun_id = Line(points=[0, 400, 80, 490], width=5)

    
    def targets(self):
        with self.canvas:
            Color(1, 0, 0, 1)
            self.y_target = []
            self.r = []
            self.targets_ids = []
            self.score = 0
            rand_y = randint(100, 400)
            self.y_target.append(rand_y)
            rand_r = randint(10, 40)
            self.r.append(rand_r)
            self.speed = []
            
            rand_speed = randint(100, 400)/100
            self.speed.append(rand_speed)
            for i in range(0, 5):
                while rand_y in self.y_target:
                    rand_y = randint(100, 400)
                else:
                    self.y_target.append(rand_y)

                while rand_r in self.r:
                    rand_r = randint(10, 40)
                else:
                    self.r.append(rand_r)

                while rand_speed in self.speed:
                    rand_speed = randint(100, 400)/100
                else:
                    self.speed.append(rand_speed)

            for i in range(0, 5):
                self.targets_ids.append(Ellipse(pos=(400, self.y_target[i]), size=(self.r[i], self.r[i])))

            self.move_target_clock = Clock.schedule_interval(self.move_target, 0.00625)

    def move_target(self, dt):
        for i in range(0, 5):
            self.move(self.targets_ids[i], 0, self.speed[i])
            self.collision_target(i)
    
    def collision_target(self, i):
        for i in range(0, 5):
            if abs(self.targets_ids[i].pos[1]+self.r[i] - 800) < 2:
                self.speed[i] = -self.speed[i]

            elif abs(self.targets_ids[i].pos[1]-self.r[i]) < 2:
                self.speed[i] = -self.speed[i]

    def collision_bullet_with_target(self):
        for i in range(0, 5):
            #print(((self.bullet_id.pos[0]+self.targets_ids[i].pos[0])**2 + (self.bullet_id.pos[1]+self.targets_ids[i].pos[1])**2)**0.5 - self.bullet_id.size[1] - self.r[i])
            if abs(((self.bullet_id.pos[0]-self.targets_ids[i].pos[0])**2 + (self.bullet_id.pos[1]-self.targets_ids[i].pos[1])**2)**0.5 - self.bullet_id.size[1] - self.r[i]) < 0.5:
                self.targets_ids[i].pos = [1000, 1000]

    def bullet(self, x, y):
        Color(random(), random(), random())
        self.bullet_id = (Ellipse(pos=(x, y), size=(40, 40)))
        self.speed_x = 1
        if self.tg < 0:
            self.speed_y = 1
        else:
            self.speed_y = -1
        self.collision_amount = 0
        self.bullet_exist = 1
        self.move_bullet_clock = Clock.schedule_interval(self.move_bullet, 0.00625)


    def move_bullet(self, dt):
        self.move(self.bullet_id, self.speed_x, self.speed_y)
        self.speed_y -= 0.025
        self.collision_bullet()
        self.collision_bullet_with_target()
        
        if self.collision_amount == 4:
            self.delete_bullet()


    def collision_bullet(self):
        if abs(self.bullet_id.pos[0]+self.bullet_id.size[0] - 500) < 2:
            self.collision_amount += 1
            self.speed_x = -self.speed_x
        elif abs(self.bullet_id.pos[0]-self.bullet_id.size[0]) < 2:
            self.speed_x = -self.speed_x
            self.collision_amount += 1
        abs(self.bullet_id.pos[1]-self.bullet_id.size[0])
        if abs(self.bullet_id.pos[1]+self.bullet_id.size[0] - 800) < 2:
            self.speed_y = -self.speed_y
            self.collision_amount += 1
        elif abs(self.bullet_id.pos[1]-self.bullet_id.size[0]) < 4:
            self.speed_y = -self.speed_y
            self.collision_amount += 1

    def delete_bullet(self):
        self.canvas.remove(self.bullet_id)
        self.collision_amount = 0
        self.bullet_exist = 0
        Clock.unschedule(self.move_bullet_clock)

    def loop(self, dt):
        if self.i == 0:
            self.length += 1
            tg = (400-self.touch.y) / self.touch.x;
            x1 = (self.length**2 / (1 + tg**2))**0.5;
            y1 = tg * x1;
            self.gun_id.points = [0, 400, x1, 400-y1]
                

    def on_touch_down(self, touch):
        with self.canvas:
            if self.bullet_exist == 0:
                self.touch = touch
                tg = (400-touch.y) / touch.x;
                x1 = (self.length**2 / (1 + tg**2))**0.5;
                y1 = tg * x1;
                self.gun_id.points = [0, 400, x1, 400-y1]
                self.i = 0
                self.clock = Clock.schedule_interval(self.loop, 0.05)

            
    def on_touch_move(self, touch):
        with self.canvas:
            if self.bullet_exist == 0:
                self.touch = touch
                tg = (400-touch.y) / touch.x;
                x1 = (self.length**2 / (1 + tg**2))**0.5;
                y1 = tg * x1;
                self.gun_id.points = [0, 400, x1, 400-y1]

    def on_touch_up(self, touch):
        with self.canvas:
            if self.bullet_exist == 0:
                tg = (400-touch.y) / touch.x;
                x1 = (self.length**2 / (1 + tg**2))**0.5;
                y1 = tg * x1;
                self.tg = tg
                self.bullet(x1, 400-y1)
                self.length = 100
                tg = (400-touch.y) / touch.x;
                x1 = (self.length**2 / (1 + tg**2))**0.5;
                y1 = tg * x1;
                self.gun_id.points = [0, 400, x1, 400-y1]
                Clock.unschedule(self.clock)

    def move(self, id, x, y):
        with self.canvas:
            id.pos = (id.pos[0]+x, id.pos[1]+y)

class MyApp(App):
    def build(self):
        parent = Widget()
        canvas = PainterWidget()
        parent.add_widget(canvas)
        canvas.my_init()

    
        
        return parent

if __name__ == '__main__':
    MyApp().run()

