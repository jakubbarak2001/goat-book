import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()


    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_todo_list(self):
        # Jacob has heard of a new cool on-line to do app.
        # He opens his browser to check the app's homepage
        self.browser.get("http://localhost:8000")

        #He notices that the site shows 'To-Do' in its title
        self.assertIn("To-Do", self.browser.title)

        #He is invited to enter a to-do item straight away.
        self.fail("Finish the test!")

        #There is still a text box inviting him to write a new item
        #He creates new item "Visit parents."

        #The page updates again, now showing both of the items in the to-do list
        #Satisfied, he goes to sleep

if __name__ == '__main__':
    unittest.main()