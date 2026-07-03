import unittest
from unittest.mock import patch, call, Mock
from deep_work import Deep_Work
from database import Database
from graph import Plotter
class TestDeepWork(unittest.TestCase):
   

    @patch('builtins.print')
    @patch('builtins.input')
    def test_main_menu_wrong_input_print(self, mock_input, mock_print):

        mock_input.side_effect = ["i", "3"]
        dw = Deep_Work()
        dw.main_menu()
        
        mock_print.assert_any_call("\nInput not recognized.\n")



if __name__ == "__main__":
    unittest.main()