from django.test import TestCase
from django.http import HttpRequest
from django.urls import resolve
from lists.views import home_page


class HomePageTest( TestCase ) :

    def testRootURLResolvesToHomePageView( self ) :
        found = resolve("/")
        self.assertEqual( found.func, home_page )

    def testHomePageReturnsCorrectHTML( self ):
        request = HttpRequest()
        response = home_page( request )
        html = response.content.decode('utf8')
        self.assertTrue( html.startswith('<html>'))
        self.assertIn( '<title>To-Do lists</title>', html )
        self.assertTrue( html.endswith('</html>'))


