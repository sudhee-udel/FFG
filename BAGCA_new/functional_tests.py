from selenium import webdriver
import unittest

class WebPageTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_navigate_to_home_page(self):
        # Navigate to the home page
        self.browser.get('http://localhost:8000')

        # Check that the title of the home page is what we expect
        self.assertIn('Boys & Girls Club of Delaware Training', self.browser.title)

web_testing = WebPageTest()
web_testing.setUp()

web_testing.test_navigate_to_home_page()

web_testing.tearDown()