#!/usr/bin/python
import BaseHTTPServer
import os
import shutil

import config
import DownloadQueue

HOST = config.get("host")
PORT = config.get("port")

queue = DownloadQueue.DownloadQueue()

class CGIReply:
	def __init__(self, code, mime, data):
		self.code = code
		self.mime = mime
		self.data = data

class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_HEAD(self):
		reply = CGI().dispatchRequest(self.path)
		self.send_response(reply.code)
		self.send_header("Content-type", reply.mime)
		if reply.mime.startswith("video/"):
			stat = os.stat(reply.data)
			self.send_header("Content-Length", stat.st_size)
		else:
			self.send_header("Content-Length", len(reply.data))
		self.end_headers()
		return reply

	def do_GET(self):
		reply = self.do_HEAD()
		if reply.mime.startswith("video/"):
			print "will feed video data to client"
			f = open(reply.data, 'rb')
			shutil.copyfileobj(f, self.wfile)
			f.close()
			print "done feeding video data to client"
		else:
			self.wfile.write(reply.data)

class CGI:
	def do_video(self, argv):
		if not "id" in argv:
			return CGIReply(400, "application/xml",
					"missing parameter id")
		filename = argv["id"] + ".mp4"
		try:
			os.stat(filename)
			return CGIReply(200, "video/x-flv", filename)
		except OSError:
			return CGIReply(404,
					"application/xml",
					"<xml>file not found</xml>")

	def do_status(self, argv):
		rss = \
"""<?xml version="1.0" encoding="UTF-8"?>
<status>
	<queue>"""
		for item in queue.asList():
			rss += "<item>" + item + "</item>\n"
		rss += \
"""
	</queue>
</status>
"""
		reply = CGIReply(200,
				"application/xml",
				rss)
		return reply

	def do_rss(self, argv):
		date = "Sat, 15 Jan 2015 16:50:00 GMT"
		rss = \
"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
	<channel>
		<title>Test rss feed</title>
		<link>http://FIXME.com</link>
		<description>Test rss feed (real feed to provide details on filters, etc, in title an description).</description>
		<language>sv</language>
		<pubDate>""" + date + """</pubDate>
		<lastBuildDate>""" + date + """</lastBuildDate>
		<item>
			<title>Test item 1 (not downloaded)</title>
			<description>This is a long description for item one.</description>
			<link>http://""" + HOST + ":" + str(PORT) + """/download?id=1</link>
			<pubDate>""" + date + """</pubDate>
			<guid>http://FIXME-1</guid>
			<boxee:property name="custom:state">remote</boxee:property>
		</item>
		<item>
			<title>Test item 2</title>
			<description>
			Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce sed libero ut eros fermentum convallis sed nec magna. Aliquam erat volutpat. Fusce quis euismod felis. Mauris a volutpat est. Nulla lacinia consequat massa vel imperdiet. Vestibulum gravida auctor purus, et auctor risus scelerisque quis. Proin viverra nisl ac lectus imperdiet non rutrum eros adipiscing. Donec id velit vitae orci adipiscing luctus. Duis eget enim augue. Ut metus velit, aliquet auctor convallis non, bibendum ac lacus. Pellentesque in dui ante. In et purus ut lacus semper mattis. Vestibulum dui lacus, aliquam lobortis pharetra in, convallis at lacus. Proin vulputate mauris non enim varius adipiscing. Sed odio sapien, convallis eu sollicitudin ac, tristique quis nulla. Pellentesque mi mauris, consectetur fringilla venenatis eu, semper vitae lectus.
			</description>
			<link>http://""" + HOST + ":" + str(PORT) + """/video?id=2</link>
			<pubDate>""" + date + """</pubDate>
			<guid>http://FIXME-2</guid>
			<boxee:property name="custom:state">local</boxee:property>
		</item>
		<item>
			<title>Pa sparet</title>
			<description>Weekly entertainment.</description>
			<link>http://""" + HOST + ":" + str(PORT) + """/video?id=3</link>
			<pubDate>""" + date + """</pubDate>
			<guid>http://FIXME-3</guid>
			<boxee:property name="custom:state">local</boxee:property>
		</item>
	</channel>
</rss>
"""
		reply = CGIReply(200,
				"application/xml",
				rss);
		return reply

	def dispatchRequest(self, cmdline):
		if len(cmdline) < 1 or cmdline[0] != "/":
			reply = CGIReply(400, "application/xml",
					"syntax error: '%s'" % (cmdline))
			return reply

		cmdline = cmdline.lstrip("/")

		if cmdline.find("?") != -1:
			(req, args) = cmdline.split("?", 1)
		else:
			(req, args) = (cmdline, "")

		argv = dict()
		for pair in args.split("&"):
			if len(pair) == 0:
				continue
			if pair.find("=") == -1:
				reply = CGIReply(400, "application/xml",
						"syntax error: '%s'" % (cmdline))
				return reply
			tmp = pair.split("=")
			if len(tmp) != 2:
				reply = CGIReply(400, "application/xml",
						"syntax error: '%s'" % (cmdline))
				return reply
			argv[tmp[0]] = tmp[1]

		try:
			fp = getattr(self, "do_" + req)
			return fp(argv)
		except AttributeError:
			reply = CGIReply(400, "application/xml",
					"unknown request '%s'" % (req))
			return reply

if __name__ == "__main__":
	print "server:", HOST, PORT
	httpServer = BaseHTTPServer.HTTPServer((HOST, PORT), HTTPHandler)
	httpServer.serve_forever()
	httpServer.server_close()

# vi: ts=4 sw=4 noet
