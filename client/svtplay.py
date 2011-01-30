#!/usr/bin/python
import threading
import urllib2
import xml.dom.minidom

try:
	from boxee import Play, SetListItems
except:
	from pc import Play, SetListItems

class DownloadThread(threading.Thread):
	def __init__(self, url, offset = None):
		if offset == None:
			self.url = url
		else:
			self.url = url + "?start=" + str(offset)
		self.data = None
		threading.Thread.__init__(self)

	def run(self):
		request = urllib2.Request(self.url)
		response = urllib2.urlopen(request)
		self.data = response.read()
		response.close()

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
				i['id'] = node.getElementsByTagName("svtplay:titleId")[0].childNodes[0].data.encode("utf-8")
				i['title'] = node.getElementsByTagName("title")[0].childNodes[0].data.encode("utf-8")
				i['thumbnail'] = node.getElementsByTagName("media:thumbnail")[0].getAttribute("url").encode("utf-8")
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
			SetListItems(self.items)
		elif self.state == self.STATE_TITLE:
			# FIXME: should start two workerthreads, to download search results
			# FIXME: then single out items with expected title and call SetListItems
			pass
		else:
			raise Exception("unexpected state")

	def onClick(self, index):
		print "SVTPlay.onClick", index

		if self.state == self.STATE_MAIN:
			# FIXME: should set state to STATE_TITLE, call ActivateWindow, wait for OnLoad callback

			i = self.items[index]
			# FIXME: should consult self.state; for now, do the easiest thing
			url = "http://www.svtplay.se/t/" + i['id']
			Play(url)
		else:
			raise Exception("unexpected state")

_svtplay = SVTPlay()

def OnLoad():
	global _svtplay
	_svtplay.onLoad()

def OnClick(index):
	global _svtplay
	_svtplay.onClick(index)
