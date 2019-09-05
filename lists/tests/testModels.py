from django.test import TestCase
from lists.models import Item, List

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

