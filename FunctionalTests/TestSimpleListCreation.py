from .base import FunctionalTest

class NewVisitorTest( FunctionalTest ) :

    def testCanStartAListAndRetrieveItLater( self ) :

        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage

        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists

        self.assertIn( 'To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away

        inputbox = self.getItemInputBox()
        self.assertEqual( inputbox.get_attribute('placeholder'), 'Enter a to-do item' )

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

        inputbox = self.getItemInputBox()
        self.assertEqual( inputbox.get_attribute('placeholder'), 'Enter a to-do item' )

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



