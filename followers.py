from twitch import TwitchHelix
import urllib, json
import socket
import re
import time, threading
import requests
from twitch import TwitchClient
from time import sleep
import random
import sys
from itertools import islice
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=800, period=60)
def call_user(id):
	URL = 'https://api.twitch.tv/helix/users?id=' + id
	headers2 = {
    	'Authorization': 'Bearer otborovm1rnpkw90a6vkzr405p0m90',
	}
	return requests.get(URL, headers=headers2).json()
@sleep_and_retry
@limits(calls=800, period=60)
def call_follows(id):
	URL = 'https://api.twitch.tv/helix/users/follows?to_id=' + id
	headers2 = {
    	'Authorization': 'Bearer otborovm1rnpkw90a6vkzr405p0m90',
	}
	return requests.get(URL, headers=headers2).json()
#access = requests.get("https://id.twitch.tv/oauth2/authorize?client_id=6bsoscqze3gff57uog9b97m08hmywp&redirect_uri=http://localhost:3000/&response_type=token&scope=user:edit")
#print(access.url)
headers = {
   'Authorization': 'Bearer cs650oqsk7qb0sjviz82b9vh0tj8v2',
}

response = requests.get('https://api.twitch.tv/helix/', headers=headers)

f = open("D:\\Users\\Pauldin\\Documents\\follows.txt", "w+")
client = TwitchClient(client_id='6bsoscqze3gff57uog9b97m08hmywp')
client2 = TwitchHelix(client_id='6bsoscqze3gff57uog9b97m08hmywp')
user_follows_iterator = client2.get_user_follows(page_size=100, to_id='45221274')
i=1
for user in user_follows_iterator:
	response2 = call_user(user.from_id)
	followers = call_follows(user.from_id)
	if len(response2['data'])==1 and (followers['total']>=2708):
		print(str(i) + " " + response2['data'][0]['display_name'].encode('utf-8', 'replace') + " " + str(followers['total']) + " " + response2['data'][0]['type'])
	#else:
	#	print i
	i=i+1

