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
        element = self.browser.find_element_by_id('total-wordcount')
        self.assertEqual('0', element.text)
        # Sarah is invited to enter word count data.
        element = self.browser.find_element_by_id('invitation')
        self.assertEqual('Tell us what you\'ve done!', element.text)
        # She enters a date.
        # She enters her word count for the day.
        # She selects the genre of her writing for this day.
        # She can make a note about the writing.
        inputbox = self.browser.find_element_by_name('date')
        inputbox.send_keys('2014-01-04')
        inputbox = self.browser.find_element_by_name('word-count')
        inputbox.send_keys('150')
        select = self.browser.find_element_by_tag_name('select')
        for option in select.find_elements_by_tag_name('option'):
            if option.text == 'Short fiction':
                option.click()
        inputbox = self.browser.find_element_by_name('notes')
        inputbox.send_keys('notes')
        # She can click on 'Done'
        button = self.browser.find_element_by_id('submit')
        button.click()
        # A 'well done' message is displayed.
        alert = self.browser.find_element_by_class_name('alert-success')
        self.assertEqual('Well done!', alert.text)
        # The data is now visible on the page.
        entry = self.browser.find_elements_by_css_selector('article')[0]
        heading = entry.find_element_by_tag_name('h3')
        self.assertEqual('Your writing on 04 January 2014', heading.text)
        details = entry.find_elements_by_tag_name('li')
        self.assertEquals('150 words of short fiction.', details[0].text)
        self.assertEquals('Notes: notes', details[1].text)
        # There is a link to the homepage that can be followed.
        link = self.browser.find_element_by_tag_name('a')
        self.assertEqual('Return to home page', link.text)
        link.click()
        # The homepage now displays the information.
        entry = self.browser.find_elements_by_css_selector('article')[0]
        heading = entry.find_element_by_tag_name('h3')
        self.assertEqual('Your writing on 04 January 2014', heading.text)
        details = entry.find_elements_by_tag_name('li')
        self.assertEquals('150 words of short fiction.', details[0].text)


if __name__ == '__main__':
    unittest.main()
