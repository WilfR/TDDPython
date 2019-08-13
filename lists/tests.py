from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import resolve
from lists.models import Item, List
from lists.views import home_page


########################################################################
###
###      Unit Tests
###
########################################################################


class HomePageTest( TestCase ) :

    def testUsesHomeTemplate( self ):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest( TestCase ) :

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


class NewListTest( TestCase ) :

    def testCanSaveAPostRequest( self ) :

        ### Test initial state
        self.assertEqual(Item.objects.count(), 0)

        ### Execute the Post and test expected state (side effects of Post)
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        newItem = Item.objects.first()
        self.assertEqual(newItem.text, 'A new list item')

    def testRedirectsAfterPost( self ) :
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        theList = List.objects.first()
        self.assertRedirects( response, f'/lists/{theList.id}/')
        ### self.assertEqual(response.status_code, 302)
        ### self.assertEqual(response['location'], '/lists/theOnlyListInTheWorld/')



class ListAndItemModelTest( TestCase ) :

    def testSavingAndRetrievingItems( self ) :
        theList = List()
        theList.save()

        firstItem = Item()
        firstItem.text = "The first (ever) list item"
        firstItem.list = theList
        firstItem.save()

        secondItem = Item()
        secondItem.text = "Item the second"
        secondItem.list = theList
        secondItem.save()

        savedItems = Item.objects.all()
        self.assertEqual(savedItems.count(), 2, "Number of saved items")

        savedList = List.objects.first()
        self.assertEqual( savedList, theList, "Lists of objects" )

        firstSavedItem = savedItems[0]
        secondSavedItem = savedItems[1]
        self.assertEqual( "The first (ever) list item", firstSavedItem.text )
        self.assertEqual( theList, firstSavedItem.list )
        self.assertEqual( "Item the second", secondSavedItem.text )
        self.assertEqual( theList, secondSavedItem.list )



class NewItemTest( TestCase ) :

    def testCanSaveAPOSTRequestToAnExistingList( self ) :
        correctList = List.objects.create()
        otherList = List.objects.create()

        self.client.post(f'/lists/{correctList.id}/add_item', data={'item_text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1, "Items after adding one item")
        newItem =Item.objects.first()
        self.assertEqual( newItem.text, 'A new item for an existing list' )
        self.assertEqual( newItem.list, correctList )

    def testRedirectsToListView( self ) :
        correctList = List.objects.create()
        otherList = List.objects.create()

        response = self.client.post(f'/lists/{correctList.id}/add_item', data={'item_text': 'A new item for an existing list'})

        self.assertRedirects( response, f'/lists/{correctList.id}/')

