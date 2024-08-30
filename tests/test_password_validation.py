import unittest
import requests
from unittest.mock import patch
from source.password_validation import is_password_correct, is_password_pwned, request_api

class TestPasswordValidation(unittest.TestCase):

    def test_is_password_correct_valid(self):
        self.assertTrue(is_password_correct("Valid1@Password"))

    def test_is_password_correct_too_short(self):
        self.assertFalse(is_password_correct("Short1@"))

    def test_is_password_correct_no_digit(self):
        self.assertFalse(is_password_correct("NoDigit!@"))

    def test_is_password_correct_no_uppercase(self):
        self.assertFalse(is_password_correct("noupper1@"))

    def test_is_password_correct_no_lowercase(self):
        self.assertFalse(is_password_correct("NOLOWER1@"))

    def test_is_password_correct_no_special_char(self):
        self.assertFalse(is_password_correct("NoSpecial1"))

    @patch('source.password_validation.is_password_pwned', return_value=False)
    def test_is_password_correct_not_pwned(self, mock_pwned):
        self.assertTrue(is_password_correct("Secure1@Password"))

    @patch('source.password_validation.is_password_pwned', return_value=True)
    def test_is_password_correct_pwned(self, mock_pwned):
        self.assertFalse(is_password_correct("Pwned1@Password"))

    @patch('source.password_validation.request_api', return_value="002AA9B2C3:2")
    def test_is_password_pwned_true(self, mock_request_api):
        self.assertTrue(is_password_pwned("password"))

    @patch('source.password_validation.request_api', return_value="")
    def test_is_password_pwned_false(self, mock_request_api):
        self.assertFalse(is_password_pwned("password"))

    @patch('source.password_validation.request_api', return_value=None)
    def test_is_password_pwned_api_failure(self, mock_request_api):
        self.assertFalse(is_password_pwned("password"))

    @patch('source.password_validation.requests.get')
    def test_request_api_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "test response"
        response = request_api("ABCDE")
        self.assertEqual(response, "test response")

    @patch('source.password_validation.requests.get')
    def test_request_api_failure(self, mock_get):
        mock_get.side_effect = requests.RequestException("API error")
        response = request_api("ABCDE")
        self.assertIsNone(response)

if __name__ == '__main__':
    unittest.main()
