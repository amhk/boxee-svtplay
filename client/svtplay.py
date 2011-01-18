import httplib
import xml.dom.minidom

import mc

SERVER = "192.168.0.103"
PORT = 9001

class CGIResponse:
	def __init__(self, code, mime, data):
		self.code = code
		self.mime = mime
		self.data = data

def CGIRequest(req, argv = None):
	path = "/" + req
	if argv != None:
		path += "?"
		for i in argv:
			path += i + "&"
		path = path.rstrip("&")
	conn = httplib.HTTPConnection(SERVER + ":" + str(PORT))
	conn.request("GET", path)
	rsp = conn.getresponse()
	retval = CGIResponse(rsp.status,
			rsp.getheader("Content-type", ""),
			rsp.read())
	conn.close()
	return retval

def ParseXMLStatus(data):
	try:
		doc = xml.dom.minidom.parseString(data)
		retval = []
		for item in doc.getElementsByTagName("item"):
			retval.append(item.childNodes[0].data)
		return retval
	except:
		return []

def RefreshDownloadQueue():
	rsp = CGIRequest("status")
	if rsp.code == 200:
		list = mc.GetActiveWindow().GetList($(list/download-queue))
		items = mc.ListItems()
		for label in ParseXMLStatus(rsp.data):
			print type(label)
			item = mc.ListItem()
			item.SetLabel(str(label))
			items.append(item)
		list.SetItems(items)
	# FIXME: else, print error to log?
