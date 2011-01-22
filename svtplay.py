#!/usr/bin/python
import urllib2
import xml.dom.minidom
try:
	import mc
	TARGET = "boxee"
except ImportError:
	import pc
	TARGET = "pc"

CFG_URL = 'http://svtplay.se/mobil/deviceconfiguration.xml'

def load_xml(url):
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	data = response.read()
	response.close()

	return xml.dom.minidom.parseString(data)

def parse_root(node):
	for item in node.getElementsByTagName("outline"):
		if item.nodeType == item.ELEMENT_NODE and \
				(item.getAttribute("type") == "menu" or \
				item.getAttribute("type") == "rss"):
			yield item

def parse_rss(node):
	for item in node.getElementsByTagName("item"):
		yield item
	
if __name__ == "__main__":
	if TARGET == "boxee":
		print "interactive execution not supported on boxee"
		exit(1)

	pc.init()
	pc.interactive()
	pc.destroy()
