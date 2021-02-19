from django.db.models import CharField, IntegerField, Model

class Users(Model):
	email = CharField(max_length=200)
	hash = CharField(max_length=32)
	clicks = IntegerField(default=0)