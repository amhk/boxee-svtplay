#!/usr/bin/python
import os
import sys

import svtplay

def Play(url):
	print "pc.Play", url

	os.system("gnome-www-browser %s" % url)

def SetListItems(new_items):
	print "pc.SetListItems"

	i = 0
	for item in new_items:
		print i, item.title
		i += 1

def _get_user_input():
	input = ""
	while 1:
		key = sys.stdin.read(1)
		if key == "\n":
			break
		input += key
	return input.strip()

def run():
	while 1:
		input = _get_user_input()
		if len(input) == 0:
			continue
		argv = input.split()
		cmd = argv[0]
		if len(argv) > 1:
			arg = argv[1]
		else:
			arg = None

		if cmd == "exit":
			return
		elif cmd == "click":
			svtplay.OnClick(int(arg))
		elif cmd == "right":
			svtplay.OnRight()


if __name__ == "__main__":
	print "main"
	svtplay.OnLoad()
	run()
