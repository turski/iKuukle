from modules.block_grid import Block
from jinja2 import Environment, FileSystemLoader
import feedparser
import os

env = Environment(autoescape=True,
                  loader=FileSystemLoader('modules/newsfeed/templates'))
template = env.get_template('newsfeedblock')

class NewsFeedBlock(Block):
	def __init__(self, feed_url, news_count):
		self.done = False
		self._html_ = ''
		self.feed_url = feed_url
		self.news_count = news_count

	def generate(self, lock=None):
		if lock:
			lock.acquire()
		self.feed = feedparser.parse(self.feed_url)
		self._html_ = template.render( feed=self.feed,
		                               news_count=self.news_count)
		self.done = True
		if lock:
			lock.release()