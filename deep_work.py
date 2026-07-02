from tqdm import tqdm
import time
from plyer import notification
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer
from save_deep_work_session import SaveDeepWorkSession
# import keyboard
from pynput import keyboard

welcomePhrases = []



class Deep_Work:
    def __init__(self):
        self.time=0
        self.quit_the_game = False
        self.timer_paused = False

    
    def main_menu(self):
        """asking the user what does he want"""
        try:
            user_choice = input("\nWhat is it you desire?\n\n 1. Launch a Deep Work session. \n 2. See the logs.\n 3. Quit\n")
            if user_choice == "1" or user_choice =="&":
                self.launching_timer()
            elif user_choice == "2" or user_choice =="é":
                # work in progress
                print("LOGS")
            elif user_choice == "3" or user_choice =='"':
                print("See you later!")
                return;    
            else: 
                print("\nInput not recognized.\n")
                self.main_menu()
        except KeyboardInterrupt:
            return;


    def converting_minutes_to_seconds(self):
        timer_in_seconds=self.time*60
        return timer_in_seconds


    def choosing_time(self) :
        self.time = input("\nLet's get things done today.\nEnter below the duration of today's deep work session in minutes :\n")
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
            try:
                answer = input(f"\nYou've worked for {str(self.time)} minutes.\nSave your progress (y/n): \n")
                self.asking_for_users_input(answer)
            except KeyboardInterrupt:
                return;

    def asking_for_users_input(self, answer:str):
        if answer == "o":
            time_in_hours= self.time/60
            output = SaveDeepWorkSession(time_in_hours);
            output.log_deep_work_session()
            other_answer=input("\nData saved.\nReady for another session (y/n):\n")
            if other_answer == "o":
                self.launching_timer()
            elif other_answer == "n":
                self.quit_the_game = True
        elif answer == "n":
            self.quit_the_game = True



    def displaying_progressing_bar(self, time_in_seconds:int):
        listener = keyboard.Listener(on_press=self.pausing_progress_bar)
        listener.start()
        print("\nThe deep work begins. Press 'p' to pause, then 'r' to resume.\nPress esc to quit. \n")
        try:
            for i in tqdm(range(time_in_seconds), colour="green"):
                if i>time_in_seconds:
                    break
                if self.timer_paused: 
                    while self.timer_paused:
                        pass
                elif self.quit_the_game:
                    raise KeyboardInterrupt
                else:
                    time.sleep(1)
            self.informing_timer_is_over();
        except KeyboardInterrupt:
            print("\nTimer interrompu")

    def pausing_progress_bar(self, key, event):
        try:
            if key.char =="p":
                self.timer_paused = True
            if key.char =="r":
                self.timer_paused = False
        except AttributeError:
            pass
            if key == keyboard.Key.esc:
                self.timer_paused = False
                self.quit_the_game = True
    

    def launching_timer(self):
        while not self.quit_the_game:
            self.choosing_time()
            try:
                user_ready_to_begin = input(f"\n{self.time} minutes it is.\nReady to begin ? (y/n)\n")
                if user_ready_to_begin == "y":
                    time_in_seconds = self.converting_minutes_to_seconds()
                    self.displaying_progressing_bar(time_in_seconds)
                elif user_ready_to_begin == "n":
                    self.main_menu()
            except KeyboardInterrupt:
                break;




