import unittest
from unittest.mock import patch, call, Mock
from deep_work import Deep_Work
from database import Database
from graph import Plotter
from pynput import keyboard
from collections import namedtuple
import pywinctl

class TestDeepWork(unittest.TestCase):
   

    @patch('builtins.print')
    @patch('builtins.input')
    def test_main_menu_wrong_input_print(self, mock_input, mock_print):

        mock_input.side_effect = ["i", "3"]
        dw = Deep_Work()
        dw.main_menu()
        
        mock_print.assert_any_call("\nInput not recognized.\n")


    @patch('builtins.print')
    @patch('builtins.input')
    def test_choosing_wrong_time_wrong_input(self, mock_input, mock_print):
        mock_input.side_effect = ["a", "1"]
        dw = Deep_Work()
        dw.choosing_time()

        mock_print.assert_any_call("\nOnly numerics authorized.\n")

    @patch('builtins.print')
    @patch('builtins.input')
    def test_choosing_wrong_time_empty_input(self, mock_input, mock_print):
        mock_input.side_effect = ["", "1"]
        dw = Deep_Work()
        dw.choosing_time()

        mock_print.assert_any_call("\nNo empty inputs.\n")


    @patch('builtins.input')
    def test_launching_timer_with_theme(self, mock_input):
        mock_input.side_effect = ["1", "1", "coding", "n", "3"]
        dw= Deep_Work()
        dw.main_menu()

        self.assertEqual(int(dw.time), 1)
        self.assertEqual(dw.theme, "coding")



    @patch('builtins.input')
    def test_launching_timer_without_theme(self, mock_input):
        mock_input.side_effect = ["1", "1", "", "n", "3"]
        dw= Deep_Work()
        dw.main_menu()

        self.assertEqual(int(dw.time), 1)
        self.assertEqual(dw.theme, '')


    @patch('builtins.print')
    @patch('builtins.input')
    def testing_pausing_timer(self, mock_input, mock_print):
        mock_input
        dw = Deep_Work()
        dw.current_window = pywinctl.getActiveWindowTitle()
        fake_key_press = namedtuple('Key', ['char'])
        p_key = fake_key_press(char='p')
        dw.pausing_progress_bar(p_key)

        self.assertEqual(dw.timer_paused, True)


    @patch('builtins.print')
    @patch('builtins.input')
    def testing_resuming_timer(self, mock_input, mock_print):
        mock_input
        dw = Deep_Work()
        fake_key_press = namedtuple('Key', ['char'])
        p_key = fake_key_press(char='r')
        dw.pausing_progress_bar(p_key)

        self.assertEqual(dw.timer_paused, False)


if __name__ == "__main__":
    unittest.main()