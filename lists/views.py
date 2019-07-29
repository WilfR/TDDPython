from django.shortcuts import render
from django.http import HttpResponse


def home_page( request ) :
    ### if request.method == "POST" :
    ###     return HttpResponse(request.POST["item_text"])
    theDict={'new_item_text': request.POST.get('item_text', ''),}
    ### theDict={'new_item_text': request.POST.get('item_text', None),}
    return render( request, 'home.html', theDict)
    ###     {'new_item_text': request.POST.get('item_text', ''),}



