from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from pathlib import Path
import time
from django.test import LiveServerTestCase

MAX_WAIT = 5


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        options = Options()
        snap_firefox = Path("/snap/firefox/current/usr/lib/firefox/firefox")
        if snap_firefox.exists():
            options.binary_location = str(snap_firefox)
        self.browser = webdriver.Firefox(options=options)

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)


    def test_can_start_a_todo_list(self):
        # Jacob has heard of a new cool on-line to do app.
        # He opens his browser to check the app's homepage
        self.browser.get(self.live_server_url)

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
        self.wait_for_row_in_list_table("1: study python")

        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn("1: study python", [row.text for row in rows])

        #There is still a text box inviting him to write a new item
        #He creates new item "Visit parents."
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Visit parents")
        inputbox.send_keys(Keys.ENTER)

        #The page updates again, now showing both of the items in the to-do list
        self.wait_for_row_in_list_table("2: Visit parents")
        self.wait_for_row_in_list_table("1: study python")

        #Satisfied, he goes to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #Jacob starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID,"id_new_item")
        inputbox.send_keys("study python")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: study python")

        #He notices that his list has a unique URL
        jacob_list_url = self.browser.current_url
        self.assertRegex(jacob_list_url, "/lists/.+")

        # Now a new user, Francis, comes along to the site

        ## We delete all the browser's cookies
        ## as a way of simulating a brand-new user session
        self.browser.delete_all_cookies()

        # Francis visits the home page. There is no sign of Jacob's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("study python", page_text)

        # Francis starts a new list by entering a new item. He is less interesting than Jacob...
        inputbox = self.browser.find_element(By.TAG_NAME, "id_new_item")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, jacob_list_url)

        # Again there is no trace of Jacob's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("study python", page_text)
        self.assertIn("Buy milk", page_text)

        #Satisfied they both go to sleep