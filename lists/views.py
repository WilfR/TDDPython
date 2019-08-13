from django.shortcuts import render, redirect
from lists.models import Item, List



def home_page( request ) :
    return render( request, 'home.html' )


def view_list( request, listID ) :
    theList = List.objects.get(id=listID)
    items = Item.objects.filter(list=theList)
    return render( request, 'list.html', { 'items' : items, 'list' : theList } )

def new_list( request ) :
    theList = List.objects.create()
    Item.objects.create( text=request.POST['item_text'], list=theList )
    return redirect(f'/lists/{theList.id}/')


def add_item( request, listID ) :
    theList = List.objects.get( id = listID )
    Item.objects.create(text=request.POST['item_text'], list=theList)
    return redirect(f'/lists/{theList.id}/')

