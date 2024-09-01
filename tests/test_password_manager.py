import unittest
from unittest.mock import MagicMock, patch
import curses
from source.password_manager import password_manager

class TestPasswordManager(unittest.TestCase):
    @patch('source.password_manager.read_data_json')
    @patch('source.password_manager.choice_function')
    @patch('source.password_manager.input_function')
    @patch('source.password_manager.show_password')
    @patch('source.password_manager.add_new_password')
    @patch('curses.color_pair')
    @patch('curses.A_BOLD', new=8)  # Mocking curses constants
    @patch('curses.A_UNDERLINE', new=16)  # Mocking curses constants
    @patch('curses.initscr')  # Ensure initscr is mocked to prevent the error
    def test_password_manager(self, mock_initscr, mock_color_pair, mock_add_new_password, mock_show_password, mock_input_function, mock_choice_function, mock_read_data_json):
        # Setup Mocks
        mock_stdscr = MagicMock()
        mock_read_data_json.return_value = {
            "accounts": {
                "test@example.com": {
                    "passwords-list": ["test1", "test2"],
                    "passwords": {
                        "test1": {"name": "Test 1"},
                        "test2": {"name": "Test 2"}
                    }
                }
            }
        }
        mock_choice_function.return_value = (0, [1, 2], False)
        mock_input_function.return_value = "test1"
        mock_color_pair.return_value = 2
        
        # Mock initscr to avoid curses initialization error
        mock_initscr.return_value = mock_stdscr

        # Call the function
        password_manager(mock_stdscr, 20, 50, "test@example.com")

        # Assertions
        mock_stdscr.clear.assert_called_once()
        mock_stdscr.addstr.assert_any_call(2, 5, 'Test 1', 26)  # 26 = 2 (color_pair) | 8 (A_BOLD)
        mock_stdscr.addstr.assert_any_call(4, 5, 'Test 2', 26)
        mock_stdscr.refresh.assert_called()
        mock_choice_function.assert_called()
        mock_input_function.assert_called()
        mock_show_password.assert_called()
        mock_add_new_password.assert_not_called()

if __name__ == '__main__':
    unittest.main()
