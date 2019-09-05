from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError



def home_page( request ) :
    return render( request, 'home.html' )


def view_list( request, listID ) :
    theList = List.objects.get(id=listID)
    items = Item.objects.filter(list=theList)
    return render( request, 'list.html', { 'items' : items, 'list' : theList } )

def new_list( request ) :
    theList = List.objects.create()
    theItem = Item.objects.create( text=request.POST['item_text'], list=theList )

    try:
        theItem.full_clean()
        theItem.save()
    except ValidationError :
        theList.delete()
        error = "You can't have an empty list item"
        return render( request, 'home.html', {'error' : error}  )

    return redirect(f'/lists/{theList.id}/')


def add_item( request, listID ) :
    theList = List.objects.get( id = listID )
    Item.objects.create(text=request.POST['item_text'], list=theList)
    return redirect(f'/lists/{theList.id}/')

