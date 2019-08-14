from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import unittest
import time


########################################################################
###
###      Functional Tests
###
########################################################################

MAX_WAIT_TIME = 10

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

    def waitForRowInListTable( self, rowText ) :
        startTime = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn( rowText, [row.text for row in rows] )
                return
            except( AssertionError, WebDriverException ) as e :
                currentTime = time.time()
                if currentTime - startTime > MAX_WAIT_TIME :
                    raise e
                time.sleep(0.5)

    def restartBrowser( self, url = None ) :
        self.browser.quit()
        self.browser = webdriver.Firefox()
        if url == None :
            url = self.live_server_url
        self.browser.get( url )


    ###
    ###         Tests
    ###

    def testCanStartAListAndRetrieveItLater( self ) :

        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage

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
        self.waitForRowInListTable('1: Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)

        self.sendTextToInputBox('Use peacock feathers to make a fly')

        # The page updates again, and now shows both items on her list

        self.waitForRowInListTable('1: Buy peacock feathers')
        self.waitForRowInListTable('2: Use peacock feathers to make a fly')


    def testMultipleUsersCanStartListsAtDifferentURLs( self ) :
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage

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
        self.waitForRowInListTable('1: Buy peacock feathers')

        edithListURL = self.browser.current_url
        self.assertRegex( edithListURL, '/lists/.+' )

        # Now a new user, Francis comes to the site. He should see
        # none of Edith's items

        self.restartBrowser()

        ### self.browser.quit()
        ### self.browser = webdriver.Firefox()
        ### self.browser.get( self.live_server_url )

        pageText = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn( 'Buy peacock feathers', pageText )
        self.assertNotIn( 'make a fly', pageText )

        # Francis starts his own list

        self.sendTextToInputBox('Get milk')
        self.waitForRowInListTable('1: Get milk')

        # Francis gets his own unique URL
        francisListURL = self.browser.current_url
        self.assertRegex( francisListURL, '/lists/.+' )
        self.assertNotEqual( francisListURL, edithListURL )

        # The list should contain Francis's items, not Edith's
        pageText = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn( 'Buy peacock feathers', pageText )
        self.assertIn( 'Get milk', pageText )

    def testLayoutAndStyling( self ) :

        self.browser.get( self.live_server_url )
        self.browser.set_window_size( 1024, 768 )

        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertAlmostEqual( inputbox.location['x'] + inputbox.size['width']/2, 512, delta=10 )

        ### start a new list and see that the input box is centered there too

        self.sendTextToInputBox('Buy peacock feathers')
        self.waitForRowInListTable('1: Buy peacock feathers')

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual( inputbox.location['x'] + inputbox.size['width']/2, 512, delta=10 )


