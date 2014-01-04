import unittest

from selenium import webdriver

class NewVisitorTestCase(unittest.TestCase):

    IMPLICIT_WAIT = 3

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(self.IMPLICIT_WAIT)

    def tearDown(self):
        self.browser.quit()

    def test_can_enter_data_and_retrieve_it_later(self):
        # Sarah opens her browser.
        # Sarah logs into the word-count-tracker site.
        self.browser.get('http://localhost:8080')
        self.assertIn('Writing Tracker', self.browser.title)
        # Sarah can see her total word count for the previous seven days.
        # Sarah is invited to enter word count data.
        # She enters a date.
        # She enters her word count for the day.
        # She selects the genre of her writing for this day.
        # She can make a note about the writing.
        # She can click on 'Done'
        # A 'well done' message is displayed.
        # The data is now visible on the page.
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main()
