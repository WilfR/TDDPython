from django.shortcuts import render
from django.http import HttpResponse


def home_page( request ) :
    response = HttpResponse('<html><title>To-Do lists</title><h1>To-Do</h1></html>')
    return response

