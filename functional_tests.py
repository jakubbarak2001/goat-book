from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import unittest

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
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        #He is invited to enter a to-do item straight away.
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        #He types "study python" into a text box
        inputbox.send_keys("study python")

        #When he hits enter, the page updates, and now the page lists
        # "1: study python" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertTrue(
         any(row.text == "1: study python" for row in rows),
          "New to-do item did not appear in table",
          )

        #There is still a text box inviting him to write a new item
        #He creates new item "Visit parents."
        self.fail("Finish the test")

        #The page updates again, now showing both of the items in the to-do list
        #Satisfied, he goes to sleep

if __name__ == '__main__':
    unittest.main()