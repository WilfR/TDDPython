from django.test import TestCase
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import resolve
from lists.views import home_page
from django.utils.html import escape

from unittest import skip


class HomePageTest( TestCase ) :

    def testUsesHomeTemplate( self ):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class NewListTest( TestCase ) :

    def testCanSaveAPostRequest( self ) :

        ### Test initial state
        self.assertEqual(Item.objects.count(), 0)

        ### Execute the Post and test expected state (side effects of Post)
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text, 'A new list item')

    def testRedirectsAfterPost( self ) :
        response = self.client.post('/lists/new', data={'text': 'A new list item'})
        theList = List.objects.first()
        self.assertRedirects( response, f'/lists/{theList.id}/')


    def testInvalidListItemsAreNotSaved( self ) :
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(List.objects.count(), 0)

        response = self.client.post('/lists/new', data={'text': ''})

        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(List.objects.count(), 0)

    @skip
    def testInvalidListItemsAreNotSavedWithValidItems( self ) :
        self.assertEqual(Item.objects.count(), 0)
        self.assertEqual(List.objects.count(), 0)

        response = self.client.post('/lists/new', data={'text': 'Here is a new test item'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(List.objects.count(), 1)

        theList = List.objects.first()
        response = self.client.post( f'/lists/{theList.id}/', data={'text': 'Here is a second test item'})

        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(List.objects.count(), 1)

        response = self.client.post(f'/lists/{theList.id}/', data={'text': ''})

        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(List.objects.count(), 1)



    def testHomePageUsesItemForm(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

    def testInvalidInputRendersHomeTemplate( self ) :

        response = self.client.post('/lists/new', data={'text': ''})

        self.assertEqual( response.status_code, 200 )
        self.assertTemplateUsed(response, 'home.html')


    def testValidationErrorsAreShownOnHomePage( self ) :

        response = self.client.post('/lists/new', data={'text': ''})

        self.assertContains( response, escape(EMPTY_ITEM_ERROR) )

    def testInvalidInputPassesFormToTemplate( self ) :

        response = self.client.post('/lists/new', data={'text': ''})

        self.assertIsInstance( response.context['form'], ItemForm )




class ListViewTest( TestCase ) :

    def postEmptyItem( self ) :
        theList = List.objects.create()
        return self.client.post( f'/lists/{theList.id}/', data={'text': ''} )


    def testUsesListTemplate( self ):
        theList = List.objects.create()
        response = self.client.get(f'/lists/{theList.id}/')
        self.assertTemplateUsed(response, 'list.html')


    def testDisplayAllListItems( self ) :
        theList = List.objects.create()
        Item.objects.create(text='itemey 1', list=theList)
        Item.objects.create(text='itemey 2', list=theList)

        response = self.client.get(f'/lists/{theList.id}/')

        self.assertContains(response, 'itemey 1' )
        self.assertContains(response, 'itemey 2' )

    def testDisplayOnlyItemsForThatList( self ) :
        correctList = List.objects.create()
        Item.objects.create(text='itemey 1', list=correctList)
        Item.objects.create(text='itemey 2', list=correctList)
        otherList = List.objects.create()
        Item.objects.create(text='boxer 1', list=otherList)
        Item.objects.create(text='boxer 2', list=otherList)

        response = self.client.get(f'/lists/{correctList.id}/')

        self.assertContains(response, 'itemey 1' )
        self.assertContains(response, 'itemey 2' )
        self.assertNotContains( response, 'boxer' )


    def testPassesCorrectListToTemplate( self ) :
        correctList = List.objects.create()
        otherList = List.objects.create()

        response = self.client.get(f'/lists/{correctList.id}/')

        self.assertEqual( response.context['list'], correctList )


    def testCanSaveAPOSTRequestToAnExistingList( self ) :
        correctList = List.objects.create()
        otherList = List.objects.create()

        self.client.post(f'/lists/{correctList.id}/', data={'text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1, "Items after adding one item")
        newItem =Item.objects.first()
        self.assertEqual( newItem.text, 'A new item for an existing list' )
        self.assertEqual( newItem.list, correctList )

    def testPOSTRedirectsToListView( self ) :
        correctList = List.objects.create()
        otherList = List.objects.create()

        response = self.client.post(f'/lists/{correctList.id}/', data={'text': 'A new item for an existing list'})

        self.assertRedirects( response, f'/lists/{correctList.id}/')


    def testForInvalidInputNothingSavedToDB( self )  :
        self.assertEqual( Item.objects.count(), 0, "Test precondition")
        response = self.postEmptyItem()
        self.assertEqual( Item.objects.count(), 0, "Should have no items if we tried to create an invalid item")


    def testInvalidInputRendersListTemplate( self ) :
        response = self.postEmptyItem()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')


    def testForInvalidInputPassesFormToTemplate( self ) :
        response = self.postEmptyItem()
        self.assertIsInstance( response.context['form'], ItemForm )

    def testForInvalidInputShowsErrorOnPage( self ) :
        response = self.postEmptyItem()
        self.assertContains( response, escape( EMPTY_ITEM_ERROR ) )


    def testDisplaysItemForm(self):
        theList = List.objects.create()

        response = self.client.get(f'/lists/{theList.id}/')

        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')




