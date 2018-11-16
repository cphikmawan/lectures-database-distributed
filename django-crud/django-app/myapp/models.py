from mongoengine import *

class Quotes(Document):
    Auther = StringField(max_length=200)
    quote = StringField(max_length=1000)