from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError

def home_page( request ) :
    return render( request, 'home.html' )


def view_list( request, listID ) :
    theList = List.objects.get(id=listID)
    error = None

    if request.method == 'POST' :

        try:
            print("--> view_list POST processing")
            theItem = Item.objects.create(text=request.POST['item_text'], list=theList)
            print(f"--> view_list POST processing theItem created text=({theItem.text})")

            theItem.full_clean()
            print("--> view_list POST processing full_clean passed")

            theItem.save()
            print("--> view_list POST processing save passed")

            return redirect(theList)

        except ValidationError :
            print("--> view_list except ValidationError execcuted")
            error = "You can't have an empty list item"

    return render( request, 'list.html', { 'list' : theList, 'error' : error } )

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

    return redirect(theList)

