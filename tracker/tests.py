import datetime
import unittest

from . import utils


class SevenDaysBeforeTestCase(unittest.TestCase):

    def test_returns_date_of_seven_days_ago(self):
        expected = datetime.date(2014, 5, 12)
        result = utils.seven_days_before(datetime.date(2014, 5, 18))
        self.assertEqual(result, expected)

