from flask import render_template, request
from app import app
import requests
import json
import logging
import os
import base64
import memcache

logging.basicConfig(level=logging.DEBUG)

# memcache setup
memcached_host = os.environ.get('MEMCACHE_PORT_11211_TCP_ADDR')
if memcached_host is None:
	memcached_host = '127.0.0.1'
memcached_port = os.environ.get('MEMCACHE_PORT_11211_TCP_PORT')
if memcached_port is None:
	memcached_port = 11211
client = memcache.Client([(memcached_host, int(memcached_port))])

def memcached_external_api_get(url):
	b64_url = base64.b64encode(url)
	result = client.get(b64_url)
	if not result:
		result = requests.get(url).json()
		client.set(b64_url, result, time=0)
	return result

@app.route('/')
def index():
    url = "http://dnd5eapi.co/api/spells/"
    response = memcached_external_api_get(url)
    return render_template(
        "index.html",
        data=response["results"]
        )

@app.route('/details', methods=['POST'])
def details():
	url = request.form['URL']
	response = memcached_external_api_get(url)
	return render_template(
	    "details.html",
	    data=response)
	
@app.route('/classes', methods=['POST'])
def classes():
	url = request.form['URL']
	response = memcached_external_api_get(url)
	return render_template(
	    "classes.html",
	    data=response)


