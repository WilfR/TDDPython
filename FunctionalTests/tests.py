from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


########################################################################
###
###      Functional Tests
###
########################################################################


class NewVisitorTest( LiveServerTestCase ) :

    ###
    ###     Utilities
    ###

    def setUp( self ) :
        self.browser = webdriver.Firefox()

    def tearDown( self ) :
        self.browser.quit()

    def checkForRowTextInTable( self, rowText ) :
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn( rowText, [row.text for row in rows] )

    def sendTextToInputBox( self, sendText ) :
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(sendText)
        inputbox.send_keys(Keys.ENTER)

    ###
    ###         Tests
    ###

    def testCanStartAListAndRetrieveItLater( self ) :
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        ### self.browser.get('http://localhost:8000')
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn( 'To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual( inputbox.get_attribute('placeholder'), 'Enter a to do item' )

        # She types "Buy peacock feathers" into a text box
        self.sendTextToInputBox('Buy peacock feathers')
        time.sleep(1)

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table

        self.checkForRowTextInTable('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)

        self.sendTextToInputBox('Use peacock feathers to make a fly')
        time.sleep(1)
        self.checkForRowTextInTable('1: Buy peacock feathers')
        self.checkForRowTextInTable('2: Use peacock feathers to make a fly')


        self.fail('Finish the test!')

        # The page updates again, and now shows both items on her list

### if __name__ == '__main__' :
###     unittest.main(warnings='ignore')


