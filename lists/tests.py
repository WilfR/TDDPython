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

        ### Test initial state
        self.assertEqual(Item.objects.count(), 0)

        ### Execute the Post and test expected state (side effects of Post)
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text, 'A new list item')

    def testRedirectsAfterPost( self ) :
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')


    def testSavesOnlyWhenNecessary( self ) :
        self.assertEqual(Item.objects.count(), 0)
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


    def testDisplayAllListItems( self ) :
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
        response = self.client.get('/')
        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

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


