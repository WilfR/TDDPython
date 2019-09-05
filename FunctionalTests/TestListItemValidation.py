from unittest import skip

from .base import FunctionalTest

class ItemValidationTest( FunctionalTest ) :
    def testCannotAddEmptyListItems(self):

        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box

        self.browser.get(self.live_server_url)
        self.sendTextToInputBox()

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank

        self.wait_for( lambda: self.assertEqual(
                           self.browser.find_element_by_css_selector('.has-error').text,
                           "You can't have an empty list item"      ) )

        # She tries again with some text for the item, which now works

        self.sendTextToInputBox('Buy milk')
        self.waitForRowInListTable('1: Buy milk')

        # Perversely, she now decides to submit a second blank list item

        self.sendTextToInputBox()

        # She receives a similar warning on the list page

        self.wait_for( lambda: self.assertEqual(
                           self.browser.find_element_by_css_selector('.has-error').text,
                           "You can't have an empty list item"      ) )


        # And she can correct it by filling some text in

        self.sendTextToInputBox('Make tea')
        self.waitForRowInListTable('1: Buy milk')
        self.waitForRowInListTable('2: Make tea')

