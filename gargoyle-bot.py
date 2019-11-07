import sys
import discord
import asyncio as aio
import aioconsole
import os
import json
import random
import time
import atexit
import schedule
import time
import threading
import functools
import datetime

schedStop = threading.Event()
def timer():
	while not schedStop.is_set():
		schedule.run_pending()
		time.sleep(1)
schedThread = threading.Thread(target=timer)
schedThread.start()

random.seed()
client = discord.Client()

f = open('path to config json file')
config = json.load(f)
f.close()

# Load JSON files

f = open(config['wotw-path'])
words = json.load(f)
f.close()

numQuotes = words['number']
quotes = words['quotes']

# Load Discord token
f = open(config['token-path'])
token = f.read()
f.close()

# Load other IDs
uID = int(config['uid'])
cID = int(config['cid'])

@client.event
async def on_ready():
	schedule.every().hour.at(':00').do(notify)
	schedule.every().hour.at(':15').do(notify)
	schedule.every().hour.at(':30').do(notify)
	schedule.every().hour.at(':45').do(notify)
	print('\nProcess ID: ' + str(os.getpid()))
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	if type(message.channel) is discord.TextChannel:
		admin = False
		for r in message.author.roles:
			if r.name == 'Admin':
				admin = True
				break
		
		if message.author == client.user:
			return
		if message.content.startswith('!'):
			ch = message.channel
			# !help
			if message.content.startswith('!help'):
				tmp = await ch.send('The following are valid commands:\n!wisdom')
			# !kill	
			elif message.content.startswith('!kill') and admin:
				tmp = await ch.send('Logging out...')
				tmp = await client.close()
				schedStop.set()
				quit()
			# !wisdom
			elif message.content.startswith('!wisdom'):		
				q = wotw()
				tmp = await ch.send('\"' + q['body'] + '\"\n- ' + q['author'])
			# Invalid	
			else:
				tmp = await ch.send('Not a valid command!')
			 
			print(time.strftime('%H:%M:%S') + '> ' + message.author.name + ' (' + str(message.author.id) + ') used command ' + message.content)

# Words of the wise

def wotw():
	i = random.randint(0, numQuotes)
	return quotes[i]

# ------

# Notification gathering

def send_notification(u, content, t):
	print('\t' + time.strftime('%H:%M:%S') + '> Starting scheduled task: send_notification')
	client.loop.create_task(u.dm_channel.send(content))

def make_dm(content, t):
	print('\t' + time.strftime('%H:%M:%S') + '> Starting scheduled task: make_dm')
	u = t.result()
	task = client.loop.create_task(u.create_dm())
	task.add_done_callback(functools.partial(send_notification, u, content))
	
def user_fetch(userID, content, t=None):
	print('\t' + time.strftime('%H:%M:%S') + '> Starting scheduled task: user_fetch')
	task = client.loop.create_task(client.fetch_user(userID))
	task.add_done_callback(functools.partial(make_dm, content))

def message_count_2(userID, aft, t):
	messages = t.result()
	aft = aft - datetime.timedelta(hours = 4)
	before = aft + datetime.timedelta(minutes = 15)
	content = aft.strftime('%b %d, %y %I:%M %p') + ' to ' + before.strftime('%I:%M %p') + ':\t' + str(len(messages)) + ' messages sent'
	
	if len(messages) > 0:
		user_fetch(userID, content)
	else:
		print('\t\t' + time.strftime('%H:%M:%S') + '> No messages sent. Cancelling')
	
def message_count_1(userID, ch):
	print('\t' + time.strftime('%H:%M:%S') + '> Starting scheduled task: message_count')
	aft = datetime.datetime.utcnow()
	aft = aft - datetime.timedelta(minutes = 15)
	task = client.loop.create_task(ch.history(after=aft).flatten())
	task.add_done_callback(functools.partial(message_count_2, userID, aft))

def notify():
	print(time.strftime('%H:%M:%S') + '> Starting scheduled task: notify')
	
	general = client.get_channel(cID)
	if general is not None:
		message_count_1(uID, general)

# ------

client.run(token)