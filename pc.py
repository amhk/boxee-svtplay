import os
import sys

import svtplay

NS_PLAYOPML = "http://xml.svtplay.se/ns/playopml"

def node_value(node, key, namespace = None):
	try:
		if namespace == None:
			return node.getElementsByTagName(key)[0].childNodes[0].data.encode("utf-8")
		else:
			return node.getElementsByTagNameNS(namespace, key)[0].childNodes[0].data.encode("utf-8")
	except:
		return ""

def get_user_input():
	input = ""
	while 1:
		key = sys.stdin.read(1)
		if key == "\n":
			break
		input += key
	return input.strip()

def do_info(argv):
	"""info ID -- show detailed information on an item"""
	global items

	try:
		item = items[int(argv[0])]
		for i in ["title", "url", "type", "ids", "thumbnail", "content"]:
			sys.stdout.write("%-9s : %s\n" % (i, item[i]))
	except:
		if len(argv) == 0:
			print "info: bad index"
		else:
			print "info: %s: bad index" % argv[0]

def do_view(argv):
	"""view ID -- open ID's URL in external browser"""
	global items

	try:
		item = items[int(argv[0])]
		if len(item["url"]) == 0:
			print "view: item has no url"
			return
		os.system("gnome-www-browser %s" % item["url"])
	except:
		if len(argv) == 0:
			print "view: bad index"
		else:
			print "view: %s: bad index" % argv[0]

def impl_cd(url):
	global items

	sys.stdout.write("(http...)")
	sys.stdout.flush()
	del items[:]
	node = svtplay.load_xml(url)
	if url == svtplay.CFG_URL:
		tmp = svtplay.parse_root(node)
		for item in tmp:
			a = dict()
			a["title"] = item.getAttribute("text").encode("utf-8")
			a["url"] = item.getAttribute("xmlUrl").encode("utf-8")
			a["type"] = item.getAttribute("type").encode("utf-8")
			a["ids"] = item.getAttributeNS(NS_PLAYOPML, "contentNodeIds").encode("utf-8")
			a["thumbnail"] = item.getAttribute("svtplay:thumbnail").encode("utf-8")
			a["content"] = ""
			items.append(a)
	else:
		for item in svtplay.parse_rss(node):
			a = dict()
			a["title"] = node_value(item, "title")
			a["url"] = node_value(item, "link")
			a["type"] = "video"
			a["ids"] = node_value(item, "ids")
			a["thumbnail"] = node_value(item, "thumbnail", "media")
			a["content"] = node_value(item, "content", "media")
			items.append(a)

	sys.stdout.write("\r         \r")

def do_cd(argv):
	"""cd ID -- change path to another item"""
	global items, path

	if len(argv) == 0:
		path = "/"
		impl_cd(svtplay.CFG_URL)
		return

	try:
		item = items[int(argv[0])]
	except:
		print "cd: %s: bad index" % argv[0]
		return
	if len(item["url"]) == 0:
		print "cd: %s: no url" % argv[0]
		return
	if item["type"] == "video":
		print "cd: %s: type is video, cannot change directory" % argv[0]
		return
	# FIXME: if has ids, don't use url as is
	path += item["title"] + "/"
	impl_cd(item["url"])

def pretty_print_type(type):
	set = { "menu" : "M", "rss" : "R", "item" : "I", "video" : "V" }
	try:
		return set[type]
	except:
		return "?"

def do_ls(argv):
	"""ls -- list current items"""

	i = 0
	for item in items:
		title = item["title"]
		url = item["url"]
		type = item["type"]
		ids = item["ids"]
		sys.stdout.write("%3d %s%s%s %s\n" % (i, len(url) > 0 and "U" or "-",
			pretty_print_type(type), len(ids) > 0 and "I" or "-", title))
		i += 1

def do_help(argv):
	"""help -- display this help"""

	for i in globals():
		if i.startswith("do_"):
			fp = globals()[i]
			print "%s" % fp.__doc__
	print "exit -- quit program"


def init():
	global items, path

	items = []
	path = "/"

def interactive():
	global items, path

	impl_cd(svtplay.CFG_URL)
	while 1:
		sys.stdout.write("%s (%d) $ " % (path, len(items)))
		input = get_user_input()
		if len(input) == 0:
			continue
		cmd = input.split()[0]
		argv = input.split()[1:]
	
		if cmd == "exit":
			return
	
		try:
			globals()['do_' + cmd](argv)
		except KeyError:
			print "%s: command not found" % cmd

def destroy():
	pass
