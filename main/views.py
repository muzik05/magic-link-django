from django.test import Client
from base64 import b64encode
from os import environ
from time import time
from hashlib import sha1

from django.views.decorators.http import require_POST
from django.shortcuts import render

from .models import Users

def index(req):
	users = Users.objects.all()
	return render(req, 'index.html',{'users':users})

@require_POST
def send_magic(req):
	if 'email' not in req.POST:
		return render(req, 'res.html',{'err':'Empty Mail Address'})
	hash = hash(req.POST['email'])
	if send_mail(email,hash):
		user = Users.objects.filter(email=email)
		if user.count()==0:
			Users.objects.create(email=email,hash=hash)
		else:
			user[0].hash = hash
			user[0].save()
		return render(req, 'res.html',{'err':'Email Sended to '+email+'. Check spam dir.'})
	else:
		return render(req, 'res.html',{'err':'Something wrong. Email dont send.'})

def check_magic(req,hash):
	user = Users.objects.filter(hash=hash)
	if user.count()==0:
		return render(req, 'res.html',{'err':'Failed Magic Hash. Email associated with this link dont exist.'})
	else:
		user[0].clicks += 1
		user[0].save()
		return render(req, 'res.html',{'err':'Success increate clicks for '+user[0].email})

def send_mail(email,hash):
	site = environ['MAILGUN-SITE']
	key = environ['MAILGUN-KEY']
	c = Client()
	try:
		return 1 if c.post("https://api.mailgun.net/v3/"+site+"/messages", {"from": "<magic@"+site+">", "to": ["User", email], "subject": "Hello man", "text": "Link https://magic-link-counter.herokuapp.com/check_magic/"+str(hash)+'/'}, HTTP_AUTHORIZATION='Basic ' + b64encode('api:'+str(key))).status_code==200 else 0
	except:
		return 0

def hash(email):
		hash = sha1()
		hash.update((email+str(time())).encode())
		return hash.hexdigest()