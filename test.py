import unittest
from unittest.mock import patch
import datetime
from graph import Plotter
from database import Database

class TestDeepWork(unittest.TestCase):

    def test_remove_redundant_dates(self):
        plot = Plotter()
        raw_data= [
            (45, datetime.date(2026, 6, 29), 'Git Merge Conflict Resolution'), 
            (110, datetime.date(2026, 6, 30), 'Database Schema Migration'), 
            (60, datetime.date(2026, 7, 1), 'Python String Manipulation'), 
            (30, datetime.date(2026, 7, 1), 'Project Dashboard Review'), 
            (90, datetime.date(2026, 7, 2), 'Refactoring Session Logic'), 
            (45, datetime.date(2026, 7, 2), 'Debugging Timestamps'), 
            (60, datetime.date(2026, 7, 2), 'Reviewing Data Types'), 
            (1, datetime.date(2026, 7, 4), ''), 
            (1, datetime.date(2026, 7, 4), ''), 
            (1, datetime.date(2026, 7, 4), ''), 
            (1, datetime.date(2026, 7, 4), ''), 
            (1, datetime.date(2026, 7, 4), ''), 
            (1, datetime.date(2026, 7, 6), 'coding')]

        expected_ouput = [
            (45, datetime.date(2026, 6, 29)), 
            (110, datetime.date(2026, 6, 30)), 
            (90, datetime.date(2026, 7, 1)), 
            (195, datetime.date(2026, 7, 2)), 
            (5, datetime.date(2026, 7, 4)),
            (1, datetime.date(2026, 7, 6))
            ]

        data = plot.remove_redundant_dates(raw_data)
        self.assertEqual(data, expected_ouput)

    @patch('builtins.print')
    def test_prep_data_for_graph_not_enough_data(self, mock_print):

        raw_data = [
            (45, '2026-06-12 09:15:00', 'Python Datetime Practice'), 
            (60, '2026-06-13 14:20:15', 'SQLite Database Setup'), 
            (30, '2026-06-15 11:05:42', 'UI Design Tweaks'), 
            (90, '2026-06-16 16:30:00', 'Backend API Refactoring'), 
            (50, '2026-06-18 10:00:12', 'Writing Documentation'), 
            (45, '2026-06-19 08:45:33', 'Bug Fixing: Auth Flow'), 
            (120, '2026-06-21 13:10:22', 'Core Algorithm Optimization'), 
            (60, '2026-06-22 15:40:55', 'Code Review & Cleanup'), 
            (40, '2026-06-24 09:25:11', 'CSS Styling Refresh'), 
            (75, '2026-06-25 11:15:00', 'SQL Query Tuning'), 
            (30, '2026-06-26 08:30:45', 'Daily Planning & Setup'), 
            (90, '2026-06-26 14:00:20', 'Feature: Dark Mode'), 
            (60, '2026-06-28 10:50:18', 'Testing Framework Setup'), 
            (45, '2026-06-29 16:15:37', 'Git Merge Conflict Resolution'), 
            (110, '2026-06-30 09:00:05', 'Database Schema Migration'), 
            (60, '2026-07-01 11:45:29', 'Python String Manipulation'), 
            (30, '2026-07-01 15:22:14', 'Project Dashboard Review'), 
            (90, '2026-07-02 08:30:00', 'Refactoring Session Logic'), 
            (45, '2026-07-02 11:10:43', 'Debugging Timestamps'), 
            (60, '2026-07-02 12:47:29', 'Reviewing Data Types'), 
            (1, '2026-07-04 08:07:32', ''), 
            (1, '2026-07-04 08:12:03', ''), 
            (1, '2026-07-04 08:13:24', ''), 
            (1, '2026-07-04 08:21:39', ''), 
            (1, '2026-07-04 08:29:17', ''), 
            (1, '2026-07-06 07:40:38', 'coding'), 
            (1, '2026-07-07 08:31:13', 'coding')
        ]


        gr = Plotter()
        gr.prep_data_for_graph(raw_data)
        mock_print.assert_any_call("\nNot enough data to plot a chart. Here's the raw data instead:\n")


    @patch('builtins.print')
    def test_search_entry_wrong_filter(self, mock_print):
        wrong_filter = "hours"
        search_input = ""
        db = Database()
        db.search_entry(wrong_filter, search_input)
        mock_print.assert_any_call("Wrong filter")

    

    def test_insert_entry(self):
        raw_data = [(1, 'coding')]
        db = Database()
        output = db.insert_entry(raw_data)

        self.assertEqual(output, [(1, 'coding')] )


if __name__ == "__main__":
    unittest.main()