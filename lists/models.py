from django.db import models

# Create your models here.

class ItemList :
    def __init__(self) :
        self.objects = []
    def all( self ) :
        return self
    def count( self ) :
        return len( self.objects )
    def addItem( self, item ) :
        self.objects.append(item)
    def __getitem__( self, i ) :
        return self.objects[i]

class Item():
    objects = ItemList()
    def __init__( self ) :
        self.text = None
    def save( self ) :
        Item.objects.addItem( self )
