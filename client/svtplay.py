#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import urllib # urllib2 in python 2.4 lacks quote function
import urllib2
import xml.dom.minidom

try:
	from boxee import Play, SetListItems, ActivateWindow
	from boxee import ID_LIST_MAIN, ID_LIST_TITLE, ID_WINDOW_TITLE
except:
	from pc import Play, SetListItems, ActivateWindow
	from pc import ID_LIST_MAIN, ID_LIST_TITLE, ID_WINDOW_TITLE

class DownloadThread(threading.Thread):
	def __init__(self, url, offset = None):
		if offset == None:
			self.url = url
		else:
			self.url = url + "&start=" + str(offset)
		self.data = None
		threading.Thread.__init__(self)

	def run(self):
		try:
			print "url:" + self.url
			request = urllib2.Request(self.url)
			response = urllib2.urlopen(request)
			self.data = response.read()
			response.close()
		except:
			print "http download failed, url=" + self.url

class WorkerThread(threading.Thread):
	TYPE_MENU = 0

	def __init__(self, url, type):
		self.url = url
		self.type = type
		self.items = []
		threading.Thread.__init__(self)

	def parseXml(self, root):
		items = []
		if self.type == self.TYPE_MENU:
			for node in root.getElementsByTagName("item"):
				i = {}
				try:
					i['guid'] = node.getElementsByTagName("guid")[0].childNodes[0].data.encode("utf-8")
					i['title'] = node.getElementsByTagName("title")[0].childNodes[0].data.encode("utf-8")
					try: # FIXME: this is too messy to stand, clean up!
						i['showtitle'] = node.getElementsByTagName("svtplay:titleName")[0].childNodes[0].data.encode("utf-8")
					except:
						i['showtitle'] = ""
					i['thumbnail'] = node.getElementsByTagName("media:thumbnail")[0].getAttribute("url").encode("utf-8")
				except:
					i['guid'] = "(error)"
					i['title'] = "(error)"
					i['thumbnail'] = "(error)"
				items.append(i)
		else:
			raise Exception("unexpected type")
		return items

	def run(self):
		firstThread = DownloadThread(self.url)
		firstThread.start()
		firstThread.join()

		root = xml.dom.minidom.parseString(firstThread.data)
		total_results = int(root.getElementsByTagName("opensearch:totalResults")[0].childNodes[0].data)
		self.items += self.parseXml(root)
		n = len(self.items)

		if n < total_results:
			# FIXME: should limit number of spawned threads and instead loop if
			# necessary?
			threads = []
			for i in range(n + 1, total_results, n):
				threads.append(DownloadThread(self.url, i))

			for t in threads:
				t.start()

			for t in threads:
				t.join()
				root = xml.dom.minidom.parseString(t.data)
				self.items += self.parseXml(root)

class SVTPlay:
	STATE_MAIN = 0
	STATE_TITLE = 1
	STATE_MOVING_TO_TITLE = 2

	def __init__(self):
		self.state = self.STATE_MAIN
		self.items = []

	def onLoad(self):
		print "SVTPlay.onLoad"

		if self.state == self.STATE_MAIN:
			del self.items[:]
			wt = WorkerThread("http://xml.svtplay.se/v1/title/list/96238", WorkerThread.TYPE_MENU)
			wt.start()
			wt.join()
			self.items = wt.items
			SetListItems(ID_LIST_MAIN, self.items)
		elif self.state == self.STATE_TITLE:
			i = self.items[0]
			del self.items[:]

			title = i['title']
			q = urllib.quote(title)
			url = "http://xml.svtplay.se/v1/search/96238&q=" + q

			wt0 = WorkerThread(url + "&expression=full", WorkerThread.TYPE_MENU)
			wt1 = WorkerThread(url + "&expression=sample", WorkerThread.TYPE_MENU)
			wt0.start()
			wt1.start()
			wt0.join()
			wt1.join()
			tmp = wt0.items
			tmp += wt1.items

			print "list length is " + str(len(tmp))
			for i in tmp:
				print "comparing '" + title + "' and '" + i['showtitle'] + "'"
				if i['showtitle'] == title:
					self.items.append(i)
			print "list length is " + str(len(self.items))
			SetListItems(ID_LIST_TITLE, self.items)
		else:
			raise Exception("unexpected state")

	def onUnLoad(self):
		print "SVTPlay.onUnLoad"

		# FIXME: possible to simplify things by not using MOVING_TO?
		if self.state == self.STATE_MAIN:
			pass
		elif self.state == self.STATE_TITLE:
			self.state = self.STATE_MAIN
		elif self.state == self.STATE_MOVING_TO_TITLE:
			self.state = self.STATE_TITLE
		else:
			raise Exception("unexpected state")

	def onClick(self, index):
		print "SVTPlay.onClick", index

		if self.state == self.STATE_MAIN:
			i = self.items[index]
			# FIXME: should use a stack of items mirroring the window stack?
			# today's framework for mode transitions and parameter passing  is
			# lacking in so many ways and should be improved
			self.items = [i]
			self.state = self.STATE_MOVING_TO_TITLE
			ActivateWindow(ID_WINDOW_TITLE)
		elif self.state == self.STATE_TITLE:
			i = self.items[index]
			id = i['guid'].split("/")[-1]
			url = "http://www.svtplay.se/v/" + id
			Play(url)
		else:
			raise Exception("unexpected state")

_svtplay = SVTPlay()

def OnLoad():
	global _svtplay
	_svtplay.onLoad()

def OnUnLoad():
	global _svtplay
	_svtplay.onUnLoad()

def OnClick(index):
	global _svtplay
	_svtplay.onClick(index)
