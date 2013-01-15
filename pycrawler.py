#!/usr/bin/python

import re ###############################regular expressions
import urllib ###########################for url library
from sys import argv ####################command line argument values

DEBUG = False

class Crawler(object):
	def __init__(self, web_address=None, depth=None, filename=None):
		self.web_address = web_address or 'http://google.com'
		self.depth = depth or 1
		self.filename = filename or 'crawl_result.html'
		self.links = []
		self.links_buffer = []
		self.links.append(self.web_address)

	def __str__(self):
		position = "1st"
		last_digit = str(depth)[:-1]
		if last_digit == "1":
			position = "1st"
		elif last_digit == "2":
			position = "2nd"
		elif last_digit == "3":
			position = "3rd"

		return "Crawler object that crawls up to the '%s' generation of the address." % position

	def crawl(self):
		if DEBUG:
			print 'starting to craw ...'
		self.begin_crawl_log()
		while(self.depth > 0):
			for link in self.links:
				self.log_source(link)
				self.find_all_links(link)
			self.depth -= 1
			self.links = self.links_buffer
			self.links_buffer = []

		self.end_crawl_log()


	def find_all_links(self, link):
		if DEBUG:
			print 'finding links in %s ...' % link
		for href in re.findall(r'''href=["']http[s]?[^"'\s]+\.[^"'\s]+["']''', urllib.urlopen(link).read(), re.I):
			self.log_site(href)


	def log_site(self, href):
		logfile = open(self.filename, 'a')
		href = str(href)
		link = href[6:-1]
		self.links_buffer.append(link)
		logfile.write('<a %s>%s</a><br>' % (href, link))
		logfile.close()

	def log_source(self, source):
		if DEBUG:
			print 'logging all the links in %s ...' %source
		logfile = open(self.filename, 'a')
		source = str(source)
		logfile.write('\n<h2>%s</h2>' % source)
		logfile.close()

	def begin_crawl_log(self):
		if DEBUG:
			print 'creating log file %s...' % self.filename
		logfile = open(self.filename, 'w')
		logfile.write('<html>')
		logfile.close()

	def end_crawl_log(self):
		if DEBUG:
			print 'closing log file ...'
		logfile = open(self.filename, 'a')
		logfile.write('</html>')
		logfile.close()



if __name__ == '__main__':
	depth = None
	web_address = None
	filename = None
	dump = ""

	for arg in argv:
		dump = '%s %s' % (dump, arg)
	print dump

	debugs = re.findall(r'''\s-debug\s''', dump)
	filenames = re.findall(r'''\s-f\s[^\s]+\s''', dump)
	web_addresses = re.findall(r'''\s-a\s[^\s]+\s''', dump)
	depths = re.findall(r'''\s-d\s[0-9]+\s?''', dump)

	for debug in debugs:
		DEBUG = True
		break

	for filename in filenames:
		filename = filename[4:].strip()
		break

	for web_address in web_addresses:
		web_address = web_address[4:].strip()
		break

	for depth in depths:
		depth = int(depth[4:])
		break

	if not re.findall(r'''\bhttp[s]?://''', web_address):
		web_address = 'http://%s' % web_address

	if not re.findall(r'''.html\b''', filename):
		filename = '%s.html' % filename

	print DEBUG, filename, web_address, depth
	
	crawler = Crawler(web_address, depth, filename)
	crawler.crawl()