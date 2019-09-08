from django.shortcuts import render, redirect
from lists.models import Item, List
from lists.forms import ExistingListItemForm, ItemForm
from django.core.exceptions import ValidationError

def home_page( request ) :
    return render( request, 'home.html', {'form' : ItemForm() }  )


def view_list( request, listID ) :
    theList = List.objects.get(id=listID)
    form = ExistingListItemForm(for_list = theList )

    if request.method == 'POST' :
        form = ExistingListItemForm( for_list = theList, data=request.POST )
        if form.is_valid() :
            form.save()
            return redirect( theList )

    return render( request, 'list.html', { 'list' : theList, 'form' : form  } )

def new_list( request ) :
    form = ItemForm(data=request.POST)
    if form.is_valid() :
        theList = List.objects.create()
        form.save( for_list = theList )
        return redirect( theList )
    else :
        return render( request, 'home.html', {'form' : form }  )

