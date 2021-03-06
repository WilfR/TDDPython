from unittest import skip

from .base import FunctionalTest

class ItemValidationTest( FunctionalTest ) :

    def getErrorElement( self ) :
       return self.browser.find_element_by_css_selector('.has-error')

    def testCannotAddEmptyListItems(self):

        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box

        self.browser.get(self.live_server_url)
        self.sendTextToInputBox()

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank

        self.wait_for( lambda: self.browser.find_element_by_css_selector('#id_text:invalid') )

        # She tries again with some text for the item, which now works

        self.sendTextToInputBox('Buy milk')
        self.wait_for( lambda: self.browser.find_element_by_css_selector('#id_text:valid') )

        self.waitForRowInListTable('1: Buy milk')

        # Perversely, she now decides to submit a second blank list item

        self.sendTextToInputBox()

        # She receives a similar warning on the list page

        self.wait_for( lambda: self.browser.find_element_by_css_selector('#id_text:invalid') )

        # And she can correct it by filling some text in

        self.sendTextToInputBox('Make tea')
        self.waitForRowInListTable('1: Buy milk')
        self.waitForRowInListTable('2: Make tea')



    def testCannotAddDuplicateItems(self):

        # Edith goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.sendTextToInputBox('Buy wellies')
        self.waitForRowInListTable('1: Buy wellies')

        # She accidentally tries to enter a duplicate item
        self.sendTextToInputBox('Buy wellies')

        # She sees a helpful error message
        self.wait_for(lambda: self.assertEqual( self.getErrorElement().text,"You've already got this in your list" ))


    def testErrorMessagesAreClearedOnInput(self):

        # Edith starts a list and causes a validation error:
        self.browser.get(self.live_server_url)

        self.sendTextToInputBox('Banter too thick')
        self.waitForRowInListTable('1: Banter too thick')

        self.sendTextToInputBox('Banter too thick')

        self.wait_for(lambda: self.assertTrue( self.getErrorElement().is_displayed() ))

        # She starts typing in the input box to clear the error
        self.getItemInputBox().send_keys('a')

        # She is pleased to see that the error message disappears
        self.wait_for(lambda: self.assertFalse( self.getErrorElement().is_displayed() ))

