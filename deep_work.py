from tqdm import tqdm
import time
from plyer import notification
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer
from save_deep_work_session import SaveDeepWorkSession

class Deep_Work:
    def __init__(self):
        self.time=0
        self.quit_the_game = False
    

    def converting_minutes_to_seconds(self):
        timer_in_seconds=self.time*60
        return timer_in_seconds


    def choosing_time(self) :
        self.time = input("\nHow long :\n")
        if not self.time or self.time == "":
            print("\nNo empty inputs.\n")
            self.choosing_time()
        try:
            self.time = int(self.time)
        except ValueError:
            print("\nOnly numerics authorized.\n")
            self.choosing_time()
     

    def playing_notification_sound(self):
        mixer.init()
        mixer.music.load("timer_over")
        mixer.music.play();

    def informing_timer_is_over(self):
            self.playing_notification_sound();
            notification.notify(
            title='Deep Work',
            message='Work session over !',
            )
            answer = input(f"\nYou've worked for {str(self.time)} minutes.\n\nSave your progress ?\no for yes, n pour no : \n")
            self.asking_for_users_input(answer)

    def asking_for_users_input(self, answer:str):
        if answer == "o":
            output = SaveDeepWorkSession(self.time);
            output.log_deep_work_session()
            other_answer=input("\nData saved.\nReady for another session ?\no for yes, n for no : \n")
            if other_answer == "o":
                self.launching_timer()
            elif other_answer == "n":
                self.quit_the_game = True
        elif answer == "n":
            self.quit_the_game = True



    def displaying_progressing_bar(self, time_in_seconds:int):
        try:
            for i in tqdm(range(time_in_seconds), colour="green"):
                if i>time_in_seconds:
                    break;
                time.sleep(1)
                i+=1
            self.informing_timer_is_over();
        except KeyboardInterrupt:
            print("Timer interrompu")

    def launching_timer(self):
        while not self.quit_the_game:
            self.choosing_time()
            time_in_seconds = self.converting_minutes_to_seconds()
            self.displaying_progressing_bar(time_in_seconds)




