from tqdm import tqdm
import time
from plyer import notification
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer
from database import Database
from pynput import keyboard
from graph import Plotter
import pywinctl
from rich.console import Console
import random
import questionary
from questionary import Style
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm


def handling_keyboard_interrupt(function):
    def before(*args, **kwargs):
        self = args[0]
        try:
            function(*args, **kwargs)
        except KeyboardInterrupt:
            console = Console()
            console.print(f"\n{random.choice(goodbye_messages)}", style="bold #1AFF80")
            self.quit_the_game = True
            return
    return before

class Deep_Work:
    def __init__(self):
        self.theme=None
        self.time=0
        self.quit_the_game = False
        self.timer_paused = False
        self.current_window=None
        self.console = Console()

    
   
        
    @handling_keyboard_interrupt
    def main_menu(self):
        """asking the user what does he want"""
        self.current_window = pywinctl.getActiveWindowTitle()
        user_choice = questionary.select(f"\n{random.choice(welcome_messages)}\n", choices=["1. Launch a Deep Work session.", "2. See the logs.", "3. Quit" ], qmark="", style=custom_style_welcome).ask()

        if user_choice == "1. Launch a Deep Work session.":
            self.launching_timer()
        elif user_choice == "2. See the logs.":
            # work in progress
            db = Database()
            data = db.read_all_entries()
            plot = Plotter()
            plot.plotting_deep_work_session(data)

        elif user_choice == "3. Quit":
            raise KeyboardInterrupt
        else: 
            raise KeyboardInterrupt



    def converting_minutes_to_seconds(self):
        timer_in_seconds=self.time*60
        return timer_in_seconds


    def choosing_time(self) :
        self.time = IntPrompt.ask("\n[bold #1AFF80]How long (in minutes)[/]")

     

    def choosing_theme(self):
        self.theme = Prompt.ask("\n[bold #1AFF80]What are you working on (optional)[/]")
        
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
            answer = self.console.input(f"\nYou've worked for {str(self.time)} minute(s).\nSave your progress ? (y/n): \n")
            self.asking_for_users_input(answer)

    def asking_for_users_input(self, answer:str):
        if answer == "y":
            entry = (self.time, self.theme)
            arr = []
            arr.append(entry)
            db = Database()
            db.insert_entry(arr)
            other_answer=self.console.input("\nData saved.\nReady for another session (y/n):\n")
            if other_answer == "y":
                self.launching_timer()
            elif other_answer == "n":
                self.quit_the_game = True
                raise KeyboardInterrupt
        elif answer == "n":
            self.quit_the_game = True
            raise KeyboardInterrupt
        else:
            print("\nWrong input.\n")
            self.informing_timer_is_over()



    def displaying_progressing_bar(self, time_in_seconds:int):
        listener = keyboard.Listener(on_press=self.pausing_progress_bar)
        listener.start()
        self.console.print(Panel("\nThe deep work begins. Press 'p' to pause, then 'r' to resume.\nPress esc to quit. \n", style="yellow"))
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
        listener.stop()
        time.sleep(0.1)
        self.flush_input()
        self.informing_timer_is_over();


    def pausing_progress_bar(self, key):
        """only executed if the user is on the terminal"""
        if pywinctl.getActiveWindowTitle() == self.current_window:
            try:
                if key.char =="p":
                    self.timer_paused = True
                if key.char =="r":
                    self.timer_paused = False
            except AttributeError:
                print(key)
                if key == keyboard.Key.esc:
                    self.timer_paused = False
                    self.quit_the_game = True
                    return False

    def flush_input(self):
        """required to flush the inputs from listener"""
        try:
            import msvcrt
            # Sous Windows : on lit tout ce qui est dans le tampon jusqu'à ce qu'il soit vide
            while msvcrt.kbhit():
                msvcrt.getch()
        except ImportError:
            import sys
            from termios import tcflush, TCIFLUSH
            # Sous Linux/macOS : on vide le tampon d'entrée standard
            tcflush(sys.stdin, TCIFLUSH)

    def launching_timer(self):
        while not self.quit_the_game:
            self.choosing_time()
            self.choosing_theme()
            if self.theme:
                self.console.print(f"\n[bold #1AFF80]You've chosen:[/]\n[#FFAA00 not bold]·{self.time} minute(s) of work\n·{self.theme}.[/]")
                user_ready_to_begin = questionary.select("\nReady to begin ?", choices=["Yes", "No (to main menu)"],  qmark="", style=custom_style_confirm_choices).ask()
            else:
                self.console.print(f"\n[bold #1AFF80]You've chosen:[/]\n[#FFAA00 not bold]·{self.time} minute(s) of work\n·No work theme.[/]")
                user_ready_to_begin = questionary.select("\nReady to begin ?", choices=["Yes", "No (to main menu)"],  qmark="", style=custom_style_confirm_choices).ask()
            if user_ready_to_begin == "Yes":
                time_in_seconds = self.converting_minutes_to_seconds()
                self.displaying_progressing_bar(time_in_seconds)
            elif user_ready_to_begin == "No (to main menu)":
                self.main_menu()
                break;




welcome_messages = [
    "Hey there! Great to see you. Let's get started!",
    "Welcome! Ready to do some awesome stuff today?",
    "Hi! Hope you're having a great day. What are we building?",
    "Welcome aboard! Let's get to work. 🚀",
    "Hey! Glad you're here. Let's dive right in.",
    "Welcome back! Good to see you again.",
    "Hello! Ready when you are.",
    "Hey, welcome! Let's make something cool today."
]

goodbye_messages = [
    "Goodbye! Have a great rest of your day.",
    "All done here! Catch you later.",
    "Thanks for stopping by. See you next time!",
    "Take care! Let me know when you need me again.",
    "That's all for now. Have a good one!",
    "Signing off! Talk to you soon.",
    "Great working with you today. Bye!",
    "Everything is set. See ya!",
    "Thanks for using the script! Have an awesome day ahead.",
    "Until next time! Take it easy."
]

custom_style_welcome = Style([
    ('instruction', 'italic'),
    ('question', 'bold #1AFF80'),
    ('highlighted', 'bold')
])

custom_style_confirm_choices = Style([
    ('question', 'bold #1AFF80'),
    ('highlighted', 'bold')
])