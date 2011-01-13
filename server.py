#!/usr/bin/python
import BaseHTTPServer

HOST = "localhost"
PORT = 9000

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
		self.end_headers()
		return reply

	def do_GET(self):
		reply = self.do_HEAD()
		if reply.mime == "FIXME-something-with-video":
			# FIXME reply.data.copy-file to wfile
			pass
		else:
			self.wfile.write(reply.data)

class CGI:
	def do_status(self, argv):
		reply = CGIReply(200,
				"application/xml",
				"<xml>status<version>foo</version></xml>")
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
	httpServer = BaseHTTPServer.HTTPServer((HOST, PORT), HTTPHandler)
	httpServer.serve_forever()
	httpServer.server_close()

# vi: ts=4 sw=4 noet
