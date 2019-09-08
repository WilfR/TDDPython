from django.test import TestCase
from lists.forms import ItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm
from lists.models import Item, List

class ItemFormTest(TestCase):

    def testFormRendersItemTextInput(self):

        form = ItemForm()

        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def testFormValidationForBlankItems( self ) :

        form = ItemForm(data={'text':''})
        self.assertFalse( form.is_valid() )
        self.assertEqual( form.errors['text'], [EMPTY_ITEM_ERROR] )


    def testFormSaveHandlesSavingToAList(self):
        theList = List.objects.create()
        form = ItemForm(data={'text': 'do me'})
        newItem = form.save(for_list=theList)

        self.assertEqual(newItem, Item.objects.first())
        self.assertEqual(newItem.text, 'do me')
        self.assertEqual(newItem.list, theList)


class ExistingListItemFormTest(TestCase):

    def testFormRendersItemTextInput(self):
        theList = List.objects.create()
        form = ExistingListItemForm(for_list=theList)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def testFormValidationForBlankItems(self):
        theList = List.objects.create()
        form = ExistingListItemForm(for_list=theList, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def testFormValidationForDuplicateItems(self):
        theList = List.objects.create()
        Item.objects.create(list=theList, text='no twins!')
        form = ExistingListItemForm(for_list=theList, data={'text': 'no twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'hi'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])


