from django.test import TestCase
from django.http import HttpRequest
from django.urls import resolve
from lists.views import home_page
from django.template.loader import render_to_string


class HomePageTest( TestCase ) :

    def testHomePageReturnsCorrectHTML( self ):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


