#!/usr/bin/python
import xml.dom.minidom
import urllib2
import sys

try:
	from boxee import Play, SetListItems
except:
	from pc import Play, SetListItems

class Item:
	def __init__(self, title, type, url, description, thumbnail):
		self.title = title
		self.type = type
		self.url = url
		self.description = description
		self.thumbnail = thumbnail

	def __str__(self):
		return "{ title=%s type=%s url=%s thumbnail=%s }" % (self.title, self.type, self.url, self.thumbnail)

class State:
	def __init__(self):
		self.url = None
		self.offset = None
		#self.totalItems = None
		#self.itemsSoFar = None

_list = []
_state = State()

def OnLoad():
	print "svtplay.OnLoad"

	_load_menu("http://xml.svtplay.se/v1/title/list/96238")

def OnClick(index):
	global _list
	print "svtplay.OnClick", _list[index]

	item = _list[index]

	if item.type == "video":
		Play(item.url)
	else:
		raise Exception("unknown item type %s" % item.type)

def OnRight():
	print "svtplay.OnRight"

	if _state.offset != None:
		offset = int(_state.offset)
	else:
		offset = 1
	_load_menu(_state.url, offset + 20)

def _load_xml(url):
	print "load_xml", url
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	data = response.read()
	response.close()

	return xml.dom.minidom.parseString(data)

def _xml_data(node, tag, namespace = None):
	try:
		if namespace == None:
			return node.getElementsByTagName(tag)[0].childNodes[0].data.encode("utf-8")
		else:
			return node.getElementsByTagNameNS(namespace, tag)[0].childNodes[0].data.encode("utf-8")
	except:
		return ""

def _load_menu(url, offset = None):
	global _list, _state

	_state.url = url
	_state.offset = offset
	if offset != None:
		url += "&start=" + str(offset)

	del _list[:]
	root = _load_xml(url)
	#_state.totalItems = int(_xml_data(root, "opensearch:totalResults"))
	#_state.itemsSoFar = int(_xml_data(root, "opensearch:startIndex")) - 1
	for node in root.getElementsByTagName("item"):
		title = _xml_data(node, "title")
		url = _xml_data(node, "link")
		description = _xml_data(node, "description")
		thumbnail = node.getElementsByTagName("media:thumbnail")[0].getAttribute("url").encode("utf-8")
		_list.append(Item(title, "video", url, description, thumbnail))

	SetListItems(_list)
