from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError


class ItemModelTest( TestCase ) :

    def testDefaultItemText( self )  :
        item = Item()
        self.assertEqual( item.text, '' )

    def testStringRepresentation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')

class ListModelTest( TestCase ) :

    def testAbsoluteURL( self ) :
        theList = List.objects.create()
        self.assertEqual(theList.get_absolute_url(), f'/lists/{theList.id}/')


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

    def testDefaultItemTextIsEmpty( self ) :
        item = Item()
        self.assertEqual( item.text, '' )

    def testItemIsRelatedToList( self ) :
        theList = List.objects.create()
        item = Item()
        item.list = theList
        item.save()
        self.assertIn( item, theList.item_set.all() )

    def testCannotSaveEmptyListItem( self ) :
        theList = List.objects.create()
        item = Item( list=theList, text='')
        with self.assertRaises( ValidationError ) :
            item.save()
            item.full_clean()

    def testDuplicateItemsAreInvalid( self ) :
        theList = List.objects.create()
        Item.objects.create( text='Get some wibbler', list=theList )
        with self.assertRaises( ValidationError ) :
            item = Item( text='Get some wibbler', list=theList )
            item.full_clean()

    def testCanSaveSameItemToMultipleLists ( self ) :
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create( text='Get some wibbler', list=list1 )
        item = Item( text='Get some wibbler', list=list2 )
        item.full_clean() # should not raise an exception

    def testDuplicateItemsAreInvalidAlternativeImplementation( self ) :
        theList = List.objects.create()
        item1 = Item( text='Get some wibbler', list=theList )
        item1.full_clean()
        item1.save()
        with self.assertRaises( ValidationError ) :
            item2 = Item( text='Get some wibbler', list=theList )
            item2.full_clean()

    def testListOrderingIsPreservedUnderItemCreation(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
            )


