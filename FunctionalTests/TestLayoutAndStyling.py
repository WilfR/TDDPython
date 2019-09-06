from .base import FunctionalTest

class LayoutAndStylingTest( FunctionalTest ) :

    def testLayoutAndStyling( self ) :

        self.browser.get( self.live_server_url )
        self.browser.set_window_size( 1024, 768 )

        inputbox = self.getItemInputBox()

        self.assertAlmostEqual( inputbox.location['x'] + inputbox.size['width']/2, 512, delta=10 )

        ### start a new list and see that the input box is centered there too

        self.sendTextToInputBox('Buy peacock feathers')
        self.waitForRowInListTable('1: Buy peacock feathers')

        inputbox = self.getItemInputBox()
        self.assertAlmostEqual( inputbox.location['x'] + inputbox.size['width']/2, 512, delta=10 )

