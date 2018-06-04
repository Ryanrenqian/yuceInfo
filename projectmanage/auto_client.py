from mongoengine import *
from .models import *
import json
import requests
BaseUrl='192.168.1.186:8000/'
sample=open('example/sample.json','r')
def getdata():
    geturl = BaseUrl+'AutoTaskHandle/get/'
    response=json.loads(requests.get(geturl).text)

def postdata(data):
    posturl = BaseUrl+'AutoTaskHandle/get/'
    response = json.loads(requests.post(posturl,data).text)
