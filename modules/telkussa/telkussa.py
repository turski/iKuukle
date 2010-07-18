from modules.block_grid import Block
from jinja2 import Environment, FileSystemLoader
from threading import BoundedSemaphore, Thread
import feedparser
import os

env = Environment(autoescape=True,
                  loader=FileSystemLoader('modules/telkussa/'),
                  extensions=['jinja2.ext.loopcontrols'])
template = env.get_template('telkussa_block_template')

feed_url_base = 'http://telkussa.fi/RSS/Channel/%i'

class TelkussaBlock(Block):
	def __init__(self, channels, prog_count):
		self.done = False
		self._html_ = ''
		self.channel_list = channels
		self.prog_count = prog_count

	def generate(self, lock=None):
		if lock:
			lock.acquire()
		prog_lock = BoundedSemaphore(len(self.channel_list))
		prog_thread_pool = []
		self.feeds = {}
		for channel in self.channel_list:
			thread = Thread(target=self.parse_channel,
			                args=(channel, prog_lock) )
			thread.start()
			prog_thread_pool.append(thread)
		for thread in prog_thread_pool:
			thread.join()
		feeds = []
		for chan in self.channel_list:
			feeds.append(self.feeds[chan])
		self._html_ = template.render( feeds=feeds,
		                               prog_count=self.prog_count)
		self.done = True
		if lock:
			lock.release()

	def parse_channel(self, channel, lock):
		feed = feedparser.parse(feed_url_base % channel)
		self.feeds[channel] = feed