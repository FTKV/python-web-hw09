from mongoengine import *


class Author(Document):
    fullname = StringField(required=True, max_length=150)
    born_date = StringField(max_length=150)
    born_location = StringField(max_length=150)
    description = StringField(max_length=10000)
    meta = {"allow_inheritance": True, "collection": "authors"}


class Quote(Document):
    quote = StringField(required=True)
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=50))
    meta = {"allow_inheritance": True, "collection": "quotes"}
