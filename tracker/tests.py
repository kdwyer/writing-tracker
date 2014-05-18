import datetime
import unittest

from . import utils


class SevenDaysBeforeTestCase(unittest.TestCase):

    def test_returns_date_of_seven_days_ago(self):
        expected = datetime.date(2014, 5, 12)
        result = utils.seven_days_before(datetime.date(2014, 5, 18))
        self.assertEqual(result, expected)

class EntryValidationTestCase(unittest.TestCase):

    def test_invalid_date_is_identified(self):
        post = {
                'date': '2014-qw-04',
                'word-count': '5',
                'genre': 'academic writing',
                'notes': '',
        }
        expected = ['date']
        entry_validation = utils.EntryValidation(post)
        result = entry_validation.validate()
        self.assertEqual(result, expected)

    def test_valid_date_is_valid(self):
        post = {
                'date': '2014-03-04',
                'word-count': '5',
                'genre': 'academic writing',
                'notes': '',
        }
        expected = []
        entry_validation = utils.EntryValidation(post)
        result = entry_validation.validate()
        self.assertEqual(result, expected)

    def test_invalid_count_is_identified(self):
        post = {
                'date': '2014-03-04',
                'word-count': 'r5',
                'genre': 'academic writing',
                'notes': '',
        }
        expected = ['word-count']
        entry_validation = utils.EntryValidation(post)
        result = entry_validation.validate()
        self.assertEqual(result, expected)

