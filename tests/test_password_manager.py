# pylint: disable=C
import unittest
import curses
import json
import hashlib
import datetime
from unittest.mock import patch, MagicMock, Mock, mock_open
from source.password_manager import password_manager, register, sign_in, choice_function, input_function, add_new_password, safe_new_password_data, show_password, hash_password, delete_password, safe_changed_data, safe_register_data

class TestPasswordManager(unittest.TestCase):
    @patch('source.password_manager.read_data_json')
    @patch('source.password_manager.choice_function')
    @patch('source.password_manager.input_function')
    @patch('source.password_manager.show_password')
    @patch('source.password_manager.add_new_password')
    def test_password_manager_view_password(self, mock_add_new_password, mock_show_password, mock_input_function, mock_choice_function, mock_read_data_json):
        mock_read_data_json.return_value = {
            "accounts": {
                "test@example.com": {
                    "passwords-list": ["site1", "site2"],
                    "passwords": {
                        "site1": {"name": "Site 1"},
                        "site2": {"name": "Site 2"}
                    }
                }
            }
        }
        stdscr = MagicMock()
        height = 25
        width = 80
        mail = "test@example.com"
        mock_choice_function.return_value = (0, [1, 2], False)
        mock_input_function.return_value = "site1"
        password_manager(stdscr, height, width, mail)
        mock_show_password.assert_called_once_with(stdscr, mock_read_data_json.return_value, mail, "site1", height//2, width//2, height, width)
        mock_add_new_password.assert_not_called()
    @patch('source.password_manager.read_data_json')
    @patch('source.password_manager.choice_function')
    @patch('source.password_manager.add_new_password')
    def test_password_manager_add_password(self, mock_add_new_password, mock_choice_function, mock_read_data_json):
        mock_read_data_json.return_value = {
            "accounts": {
                "test@example.com": {
                    "passwords-list": ["site1", "site2"],
                    "passwords": {
                        "site1": {"name": "Site 1"},
                        "site2": {"name": "Site 2"}
                    }
                }
            }
        }
        stdscr = MagicMock()
        height = 25
        width = 80
        mail = "test@example.com"
        mock_choice_function.return_value = (1, [1, 2], False)
        password_manager(stdscr, height, width, mail)
        mock_add_new_password.assert_called_once_with(stdscr, mail, height, width, height//2, width//2)
    @patch('source.password_manager.is_mail_correct')
    @patch('source.password_manager.is_password_correct')
    @patch('source.password_manager.input_function')
    @patch('source.password_manager.choice_function')
    @patch('source.password_manager.safe_register_data')
    @patch('source.password_manager.start_screen')
    def test_register_success(self, mock_start_screen, mock_safe_register_data, mock_choice_function, mock_input_function, mock_is_password_correct, mock_is_mail_correct):
        stdscr = MagicMock()
        height = 25
        width = 80
        mock_choice_function.side_effect = [(0, [1, 2, 2, 2], False), (1, [1, 2, 2, 2], True), (2, [1, 2, 2, 2], True)]
        mock_input_function.side_effect = ["test@example.com", "StrongPass1!", "StrongPass1!"]
        mock_is_mail_correct.return_value = True
        mock_is_password_correct.return_value = True
        result = register(stdscr, height, width)
        self.assertEqual(result, "test@example.com")
        mock_is_mail_correct.assert_called_once_with("test@example.com")
        self.assertEqual(mock_is_password_correct.call_count, 2)
        mock_safe_register_data.assert_called_once_with("test@example.com", "StrongPass1!")
        mock_start_screen.assert_not_called()
    @patch('source.password_manager.is_mail_correct')
    @patch('source.password_manager.is_password_correct')
    @patch('source.password_manager.input_function')
    @patch('source.password_manager.choice_function')
    @patch('source.password_manager.safe_register_data')
    @patch('source.password_manager.start_screen')
    def test_register_invalid_email(self, mock_start_screen, mock_safe_register_data, mock_choice_function, mock_input_function, mock_is_password_correct, mock_is_mail_correct):
        stdscr = MagicMock()
        height = 25
        width = 80
        mock_choice_function.side_effect = [(0, [1, 2, 2, 2], False)]
        mock_input_function.side_effect = ["invalid-email"]
        mock_is_mail_correct.return_value = False
        result = register(stdscr, height, width)
        if result == "": pass
        mock_is_mail_correct.assert_called_once_with("invalid-email")
        mock_is_password_correct.assert_not_called()
        mock_safe_register_data.assert_not_called()
        mock_start_screen.assert_called_once()
    @patch('source.password_manager.is_mail_correct')
    @patch('source.password_manager.is_password_correct')
    @patch('source.password_manager.input_function')
    @patch('source.password_manager.choice_function')
    @patch('source.password_manager.safe_register_data')
    @patch('source.password_manager.start_screen')
    def test_register_mismatched_passwords(self, mock_start_screen, mock_safe_register_data, mock_choice_function, mock_input_function, mock_is_password_correct, mock_is_mail_correct):
        stdscr = MagicMock()
        height = 25
        width = 80
        mock_choice_function.side_effect = [(0, [1, 2, 2, 2], False), (1, [1, 2, 2, 2], True), (2, [1, 2, 2, 2], True)]
        mock_input_function.side_effect = ["test@example.com", "StrongPass1!", "StrongPass2!"]
        mock_is_mail_correct.return_value = True
        mock_is_password_correct.return_value = True
        result = register(stdscr, height, width)
        if result == "": pass
        mock_is_mail_correct.assert_called_once_with("test@example.com")
        self.assertEqual(mock_is_password_correct.call_count, 2)
        mock_safe_register_data.assert_not_called()
        mock_start_screen.assert_not_called()
    @patch('source.password_manager.read_data_json')
    @patch('source.password_manager.input_function')
    @patch('source.password_manager.choice_function')
    @patch('source.password_manager.start_screen')
    @patch('source.password_manager.hash_password')
    def test_sign_in_success(self, mock_hash_password, mock_start_screen, mock_choice_function, mock_input_function, mock_read_data_json):
        stdscr = MagicMock()
        height = 25
        width = 80
        mock_read_data_json.return_value = {
            "accounts": {
                "accounts-list": ["test@example.com"],
                "test@example.com": {
                    "master-password": "hashed_correct_password"
                }
            }
        }
        mock_choice_function.side_effect = [(0, [1, 2, 2], False), (1, [1, 2, 2], True)]
        mock_input_function.side_effect = ["test@example.com", "correct_password"]
        mock_hash_password.return_value = "hashed_correct_password"
        result = sign_in(stdscr, height, width)
        self.assertEqual(result, "test@example.com")
        mock_read_data_json.assert_called_once()
        mock_input_function.assert_any_call(stdscr, height // 2 - 4, width // 2 - 6, False)
        mock_input_function.assert_any_call(stdscr, height // 2, width // 2 - 6, True)
        mock_hash_password.assert_called_once_with("correct_password")
        mock_start_screen.assert_not_called()
    @patch('source.password_manager.read_data_json')
    @patch('source.password_manager.input_function')
    @patch('source.password_manager.choice_function')
    @patch('source.password_manager.start_screen')
    @patch('source.password_manager.hash_password')
    def test_sign_in_incorrect_email(self, mock_hash_password, mock_start_screen, mock_choice_function, mock_input_function, mock_read_data_json):
        stdscr = MagicMock()
        height = 25
        width = 80
        mock_read_data_json.return_value = {
            "accounts": {
                "accounts-list": ["test@example.com"],
                "test@example.com": {
                    "master-password": "hashed_correct_password"
                }
            }
        }
        mock_choice_function.side_effect = [(0, [1, 2, 2], False)]
        mock_input_function.side_effect = ["wrong@example.com"]
        result = sign_in(stdscr, height, width)
        self.assertFalse(mock_hash_password.called)
        self.assertIn("wrong@example.com", result)
        mock_read_data_json.assert_called_once()
        mock_start_screen.assert_not_called()
    @patch('source.password_manager.read_data_json')
    @patch('source.password_manager.input_function')
    @patch('source.password_manager.choice_function')
    @patch('source.password_manager.start_screen')
    @patch('source.password_manager.hash_password')
    def test_sign_in_incorrect_password(self, mock_hash_password, mock_start_screen, mock_choice_function, mock_input_function, mock_read_data_json):
        stdscr = MagicMock()
        height = 25
        width = 80
        mock_read_data_json.return_value = {
            "accounts": {
                "accounts-list": ["test@example.com"],
                "test@example.com": {
                    "master-password": "hashed_correct_password"
                }
            }
        }
        mock_choice_function.side_effect = [(0, [1, 2, 2], False), (1, [1, 2, 2], True)]
        mock_input_function.side_effect = ["test@example.com", "wrong_password"]
        mock_hash_password.return_value = "hashed_wrong_password"
        result = sign_in(stdscr, height, width)
        self.assertNotEqual(result, "test@example.com")
        mock_hash_password.assert_called_once_with("wrong_password")
        mock_read_data_json.assert_called_once()
        mock_start_screen.assert_not_called()
    @patch('source.password_manager.stdscr')
    def test_choice_function_key_down(self, mock_stdscr):
        ky = 0
        pair_number = [1, 2, 2]
        go = True
        mock_stdscr.getch.return_value = curses.KEY_DOWN
        ky, pair_number, go = choice_function(mock_stdscr, ky, pair_number, go)
        self.assertEqual(ky, 1)
        self.assertEqual(pair_number, [2, 1, 2])
        self.assertTrue(go)
    @patch('source.password_manager.stdscr')
    def test_choice_function_key_up(self, mock_stdscr):
        ky = 1
        pair_number = [2, 1, 2]
        go = True
        mock_stdscr.getch.return_value = curses.KEY_UP
        ky, pair_number, go = choice_function(mock_stdscr, ky, pair_number, go)
        self.assertEqual(ky, 0)
        self.assertEqual(pair_number, [1, 2, 2])
        self.assertTrue(go)  
    @patch('source.password_manager.stdscr')
    @patch('source.password_manager.is_sure_to_exit_program')
    def test_choice_function_escape_key(self, mock_is_sure_to_exit_program, mock_stdscr):
        ky = 0
        pair_number = [1, 2, 2]
        go = True
        mock_stdscr.getch.return_value = 27
        ky, pair_number, go = choice_function(mock_stdscr, ky, pair_number, go)
        mock_is_sure_to_exit_program.assert_called_once_with(mock_stdscr)
        self.assertEqual(ky, 0)
        self.assertEqual(pair_number, [1, 2, 2])
        self.assertTrue(go)
    @patch('source.password_manager.stdscr')
    def test_choice_function_enter_key(self, mock_stdscr):
        ky = 0
        pair_number = [1, 2, 2]
        go = True
        mock_stdscr.getch.return_value = 10
        ky, pair_number, go = choice_function(mock_stdscr, ky, pair_number, go)
        self.assertEqual(ky, 0)
        self.assertEqual(pair_number, [1, 2, 2])
        self.assertFalse(go)
    @patch('source.password_manager.stdscr')
    def test_input_function_normal_input(self, mock_stdscr):
        mock_stdscr.getch.side_effect = [ord('h'), ord('e'), ord('l'), ord('l'), ord('o'), 10]
        result = input_function(mock_stdscr, 0, 0, False)
        self.assertEqual(result, "hello")
    @patch('source.password_manager.stdscr')
    def test_input_function_password_input(self, mock_stdscr):
        mock_stdscr.getch.side_effect = [ord('h'), ord('e'), ord('l'), ord('l'), ord('o'), 10]
        result = input_function(mock_stdscr, 0, 0, True)
        self.assertEqual(result, "hello")
    @patch('source.password_manager.stdscr')
    def test_input_function_backspace(self, mock_stdscr):
        mock_stdscr.getch.side_effect = [ord('h'), ord('e'), ord('l'), curses.KEY_BACKSPACE, ord('o'), 10]
        result = input_function(mock_stdscr, 0, 0, False)
        self.assertEqual(result, "heo")
    @patch('source.password_manager.stdscr')
    def test_input_function_navigation(self, mock_stdscr):
        mock_stdscr.getch.side_effect = [ord('h'), ord('e'), ord('l'), curses.KEY_LEFT, curses.KEY_LEFT, ord('o'), 10]
        result = input_function(mock_stdscr, 0, 0, False)
        self.assertEqual(result, "hello")
    @patch('source.password_manager.stdscr')
    @patch('source.password_manager.is_sure_to_exit_program')
    def test_input_function_exit(self, mock_is_sure_to_exit_program, mock_stdscr):
        mock_stdscr.getch.side_effect = [27]
        result = input_function(mock_stdscr, 0, 0, False)
        mock_is_sure_to_exit_program.assert_called_once_with(mock_stdscr)
        self.assertEqual(result, "")
    @patch('source.password_manager.input_function')
    @patch('source.password_manager.choice_function')
    @patch('source.password_manager.safe_new_password_data')
    @patch('source.password_manager.password_manager')
    def test_add_new_password(self, mock_password_manager, mock_safe_new_password_data, mock_choice_function, mock_input_function):
        mock_choice_function.side_effect = [(0, [1, 2, 2, 2, 2, 2], False), (4, [1, 2, 2, 2, 2, 2], True)]
        mock_input_function.side_effect = ["TestName", "http://test.com", "TestNotes", "StrongPass1!"]
        mock_safe_new_password_data.return_value = None
        stdscr = Mock()
        add_new_password(stdscr, "test@example.com", 20, 80, 10, 10)
        mock_safe_new_password_data.assert_called_once()
        mock_password_manager.assert_called_once_with(stdscr, 20, 80, "test@example.com")

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=json.dumps({
        "accounts": {
            "test@example.com": {
                "passwords-list": ["TestName"],
                "passwords": {
                    "TestName": {
                        "name": "TestName",
                        "password": "hashed_password",
                        "url": "http://test.com",
                        "text": "TestNotes",
                        "oldpasswordlist": [],
                        "dateoffirstaccess": "01.01.2024 00:00",
                        "dateoflastchange": "01.01.2024 00:00"
                    }
                }
            }
        }
    }))
    def test_safe_new_password_data(self, mock_open_2):
        new_data = {
            "NewName": {
                "name": "NewName",
                "password": "new_password",
                "url": "http://new.com",
                "text": "NewNotes",
                "oldpasswordlist": [],
                "dateoffirstaccess": "02.01.2024 00:00",
                "dateoflastchange": "02.01.2024 00:00"
            }
        }
        safe_new_password_data(new_data, "test@example.com", "NewName")
        handle = mock_open_2()
        handle.write.assert_has_calls()
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=json.dumps({
        "accounts": {
            "test@example.com": {
                "passwords-list": ["TestName"],
                "passwords": {
                    "TestName": {
                        "name": "TestName",
                        "password": "hashed_password",
                        "url": "http://test.com",
                        "text": "TestNotes",
                        "oldpasswordlist": [],
                        "dateoffirstaccess": "01.01.2024 00:00",
                        "dateoflastchange": "01.01.2024 00:00"
                    }
                }
            }
        }
    }))
    def test_delete_password(self, mock_open_2):
        delete_password("test@example.com", "TestName")
        handle = mock_open_2()
        handle.write.assert_has_calls()
    @patch('source.password_manager.choice_function')
    @patch('source.password_manager.input_function')
    @patch('source.password_manager.password_manager')
    def test_show_password(self, mock_password_manager, mock_input_function, mock_choice_function):
        mock_choice_function.side_effect = [(0, [1, 2, 2, 2, 2], True)]
        mock_input_function.return_value = "Test input"
        stdscr = Mock()
        data = {
            "accounts": {
                "test@example.com": {
                    "passwords": {
                        "TestName": {
                            "name": "TestName",
                            "url": "http://test.com",
                            "text": "TestNotes",
                            "password": "hashed_password",
                            "dateoffirstaccess": "01.01.2024 00:00",
                            "dateoflastchange": "01.01.2024 00:00"
                        }
                    }
                }
            }
        }
        show_password(stdscr, data, "test@example.com", "TestName", 20, 80, 20, 80)
        mock_password_manager.assert_called_once_with(stdscr, 20, 80, "test@example.com")
    def test_hash_password(self):
        password = "StrongPass1!"
        hashed_password = hash_password(password)
        self.assertEqual(hashed_password, hashlib.sha256(password.encode()).hexdigest())
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "accounts": {
            "test@example.com": {
                "passwords-list": ["OldName"],
                "passwords": {
                    "OldName": {
                        "name": "OldName",
                        "password": "old_password",
                        "url": "http://old.com",
                        "text": "OldNotes",
                        "oldpasswordlist": ["old_password"],
                        "dateoffirstaccess": "01.01.2024 00:00",
                        "dateoflastchange": "01.01.2024 00:00"
                    }
                }
            }
        }
    }))
    def test_safe_changed_data_name_changed(self, mock_open_2):
        mail = "test@example.com"
        name = "NewName"
        url = "http://new.com"
        notes = "NewNotes"
        password = "new_password"
        old_name = "OldName"
        is_name_changed = True
        result = safe_changed_data(mail, name, url, notes, password, old_name, is_name_changed)
        if result == "": pass
        expected_data = {
            "accounts": {
                "test@example.com": {
                    "passwords-list": ["NewName"],
                    "passwords": {
                        "NewName": {
                            "name": "NewName",
                            "password": "new_password",
                            "url": "http://new.com",
                            "text": "NewNotes",
                            "oldpasswordlist": ["old_password", "new_password"],
                            "dateoffirstaccess": "01.01.2024 00:00",
                            "dateoflastchange": datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
                        }
                    }
                }
            }
        }
        handle = mock_open_2()
        handle.write.assert_has_calls_with(json.dumps(expected_data, indent=4))
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "accounts": {
            "test@example.com": {
                "passwords-list": ["Name"],
                "passwords": {
                    "Name": {
                        "name": "Name",
                        "password": "old_password",
                        "url": "http://old.com",
                        "text": "OldNotes",
                        "oldpasswordlist": ["old_password"],
                        "dateoffirstaccess": "01.01.2024 00:00",
                        "dateoflastchange": "01.01.2024 00:00"
                    }
                }
            }
        }
    }))
    def test_safe_changed_data_name_unchanged(self, mock_open_2):
        mail = "test@example.com"
        name = "Name"
        url = "http://new.com"
        notes = "NewNotes"
        password = "new_password"
        old_name = "Name"
        is_name_changed = False
        result = safe_changed_data(mail, name, url, notes, password, old_name, is_name_changed)
        if result == "": pass
        expected_data = {
            "accounts": {
                "test@example.com": {
                    "passwords-list": ["Name"],
                    "passwords": {
                        "Name": {
                            "name": "Name",
                            "password": "new_password",
                            "url": "http://new.com",
                            "text": "NewNotes",
                            "oldpasswordlist": ["old_password", "new_password"],
                            "dateoffirstaccess": "01.01.2024 00:00",
                            "dateoflastchange": datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
                        }
                    }
                }
            }
        }
        handle = mock_open_2()
        handle.write.assert_has_calls_with(json.dumps(expected_data, indent=4))
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "accounts": {}
    }))
    def test_safe_register_data(self, mock_open_2):
        mail = "test@example.com"
        password = "new_password"
        safe_register_data(mail, password)
        hashed_password = hash_password(password)
        expected_data = {
            "accounts": {
                "test@example.com": {
                    "mail": mail,
                    "master-password": hashed_password,
                    "passwords-list": [],
                    "passwords": {}
                }
            }
        }

        handle = mock_open_2()
        handle.write.assert_has_calls_with(json.dumps(expected_data, indent=4))

if __name__ == '__main__':
    unittest.main()
