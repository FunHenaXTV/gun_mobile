from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import (Color, Ellipse, Line)
from kivy.clock import Clock
from kivy.config import Config
from random import random, randint
from time import sleep




width = 1080
height = 1728

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', str(width))
Config.set('graphics', 'height', str(height))



class PainterWidget(Widget):
    
    def my_init(self):
        with self.canvas:
            self.length = 100
            self.bullet_exist = 0
            self.bullet_id = 0
            self.speed_y = 0
            self.collision_amount = 0
            self.score = 0
            self.bullet_amount = 0
            Color(1, 0, 0, 1)
            Line(points=[0, height, width, height], width=2)
            Line(points=[0, 0, width, 0], width=2)

            self.targets()
            self.gun()

    def gun(self):
        with self.canvas:
            Color(0, 1, 0, 1)
            self.gun_id = Line(points=[0, height/2, 80, height/2+15], width=5)

    
    def targets(self):
        with self.canvas:
            Color(1, 0, 0, 1)
            self.y_target = []
            self.r = []
            self.targets_ids = []
            self.score = 0
            rand_y = randint(200, height-200)
            self.y_target.append(rand_y)
            rand_r = randint(40, 100)
            self.r.append(rand_r)
            self.speed = []
            
            rand_speed = randint(200, 400)/100
            self.speed.append(rand_speed)
            for i in range(0, 5):
                while rand_y in self.y_target:
                    rand_y = randint(200, height-200)
                else:
                    self.y_target.append(rand_y)

                while rand_r in self.r:
                    rand_r = randint(40, 100)
                else:
                    self.r.append(rand_r)


                while rand_speed in self.speed:
                    rand_speed = randint(200, 400)/100
                else:
                    self.speed.append(rand_speed)

            for i in range(0, 5):
                self.targets_ids.append(Ellipse(pos=(width-100, (self.y_target[i])), size=(self.r[i], self.r[i])))
            self.move_target_clock = Clock.schedule_interval(self.move_target, 0.00625/5)

    def move_target(self, dt):
        for i in range(0, 5):
            self.move(self.targets_ids[i], 0, int(self.speed[i]*1.5))
            self.collision_target(i)
    
    def collision_target(self, i):
        for i in range(0, 5):
            if abs(self.targets_ids[i].pos[1]+self.r[i] - height) < 2*2:
                self.speed[i] = -self.speed[i]

            elif abs(self.targets_ids[i].pos[1]-self.r[i]) < 2*2:
                self.speed[i] = -self.speed[i]

    def collision_bullet_with_target(self):
        for i in range(0, 5):
            x = ((self.bullet_id.pos[0]+self.bullet_id.size[0]/2 - self.targets_ids[i].pos[0]-self.targets_ids[i].size[0]/2))**2
            y = ((self.bullet_id.pos[1]+self.bullet_id.size[0]/2 - self.targets_ids[i].pos[1]-self.targets_ids[i].size[0]/2))**2
            st = (x + y)**0.5
            if st <= self.bullet_id.size[0]/2 + self.targets_ids[i].size[0]/2:
                self.score += 1
                self.move(self.targets_ids[i], 3000, 3000)
            print(self.score)
            if self.score >= 5:
                self.game_over()
                break


    def game_over(self):
        Clock.unschedule(self.move_bullet_clock)
        Clock.unschedule(self.move_target_clock)
        self.bullet_exist = 1
        for i in self.targets_ids:
            self.canvas.remove(i)
        self.canvas.remove(self.bullet_id)
        self.canvas.remove(self.gun_id)
        del self.targets_ids
        del self.y_target
        del self.r
        del self.speed
        g.create_label()


    def bullet(self, x, y):
        Color(random(), random(), random())
        print(self.length)
        self.bullet_id = (Ellipse(pos=(x, y), size=(40+self.length/5, 40+self.length/5)))
        self.speed_x = 5
        self.speed_y = (self.speed_x * -self.tg)
        if abs(self.speed_y) > 20:
            self.speed_y = abs(self.speed_y)/self.speed_y*20
        self.bullet_exist = 1
        self.move_bullet_clock = Clock.schedule_interval(self.move_bullet, 0.00625/5)
        self.bullet_amount += 1


    def move_bullet(self, dt):
        self.move(self.bullet_id, (self.speed_x), (self.speed_y))
        self.speed_y -= 0.025
        #try:
        self.collision_bullet()
        self.collision_bullet_with_target()
        #except:
        #    pass
        if self.collision_amount == 4:
            self.delete_bullet()


    def collision_bullet(self):
        if abs(self.bullet_id.pos[0]+self.bullet_id.size[0] - width) < 5:
            self.speed_x = -self.speed_x
            self.collision_amount += 1
        elif abs(self.bullet_id.pos[0]) < 5:
            self.speed_x = -self.speed_x
            self.collision_amount += 1
        if abs(self.bullet_id.pos[1]+self.bullet_id.size[0] - height) < 10:
            self.speed_y = -self.speed_y
            self.collision_amount += 1
        elif abs(self.bullet_id.pos[1]) < 20:
            self.speed_y = -self.speed_y
            self.collision_amount += 1


    def delete_bullet(self):
        self.bullet_id.pos = [6000, 6000]
        self.collision_amount = 0
        self.bullet_exist = 0
        Clock.unschedule(self.move_bullet_clock)

    def loop(self, dt):
        if self.i == 0:
            self.length += 3
            tg = (height/2-self.touch.y) / self.touch.x;
            x1 = (self.length**2 / (1 + tg**2))**0.5;
            y1 = tg * x1;
            self.gun_id.points = [0, height/2, x1, height/2-y1]
                

    def on_touch_down(self, touch):
        with self.canvas:
            if self.bullet_exist == 0:
                self.touch = touch
                tg = (height/2-self.touch.y) / self.touch.x;
                x1 = (self.length**2 / (1 + tg**2))**0.5;
                y1 = tg * x1;
                self.gun_id.points = [0, height/2, x1, height/2-y1]
                self.i = 0
                self.clock = Clock.schedule_interval(self.loop, 0.05)

            
    def on_touch_move(self, touch):
        with self.canvas:
            if self.bullet_exist == 0:
                self.touch = touch
                tg = (height/2-self.touch.y) / self.touch.x;
                x1 = (self.length**2 / (1 + tg**2))**0.5;
                y1 = tg * x1;
                self.gun_id.points = [0, height/2, x1, height/2-y1]


    def on_touch_up(self, touch):
        with self.canvas:
            if self.bullet_exist == 0:
                tg = (height/2-self.touch.y) / self.touch.x;
                x1 = (self.length**2 / (1 + tg**2))**0.5;
                y1 = tg * x1;
                self.tg = tg
                self.bullet(x1, height/2-y1)
                self.length = 100
                tg = (height/2-self.touch.y) / self.touch.x;
                x1 = (self.length**2 / (1 + tg**2))**0.5;
                y1 = tg * x1;
                self.gun_id.points = [0, height/2, x1, height/2-y1]
                Clock.unschedule(self.clock)

    def move(self, id, x, y):
        with self.canvas:
            id.pos = (id.pos[0]+x, id.pos[1]+y)

        
class GunApp(App):
    def build(self):
        self.parent = Widget()
        self.canvas = PainterWidget()
        self.parent.add_widget(self.canvas)
        self.canvas.my_init()
        

    
        
        return self.parent

    def create_label(self):
        Color(1, 1, 1, 1)
        self.l1 = (Label(text='You have destroyed all targets with '+str(self.canvas.bullet_amount)+' bullets', font_size='45px', pos=[width/2, height/2]))
        self.parent.add_widget(self.l1)
        self.l2 = (Label(text='Do you want to restart?', font_size='45px', pos=[width/2, height/2-50]))
        self.parent.add_widget(self.l2)
        self.b1 = (Button(text='Yes', font_size='45px', pos=[width/2-70, height/2-120], on_release=self.yes_handler, size=[70*1.5, 50*1.5]))
        self.parent.add_widget(self.b1)
        self.b2 = (Button(text='No', font_size='45px', pos=[width/2+70, height/2-120], on_release=self.no_handler, size=[70*1.5, 50*1.5]))
        self.parent.add_widget(self.b2)

    def yes_handler(self, event):
        self.parent.remove_widget(self.l1)
        self.parent.remove_widget(self.l2)
        self.parent.remove_widget(self.b1)
        self.parent.remove_widget(self.b2)
        self.canvas.my_init()

    def no_handler(self, event):
        quit()


if __name__ == '__main__':
    g = GunApp()
    g.run()

