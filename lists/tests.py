from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve
from lists.models import Item
from lists.views import home_page



class HomePageTest( TestCase ) :

    def testUsesHomeTemplate( self ):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def testCanSaveAPostRequest( self ) :
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

class ItemModelTest( TestCase ) :

    def testSavingAndRetrievingItems( self ) :
        firstItem = Item()
        firstItem.text = "The first (ever) list item"
        firstItem.save()

        secondItem = Item()
        secondItem.text = "Item the second"
        secondItem.save()

        savedItems = Item.objects.all()
        self.assertEqual(savedItems.count(), 2, "Number of saved items")

        firstSavedItem = savedItems[0]
        secondSavedItem = savedItems[1]
        self.assertEqual( "The first (ever) list item", firstSavedItem.text )
        self.assertEqual( "Item the second", secondSavedItem.text )


