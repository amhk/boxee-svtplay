#!/usr/bin/python
import os
import sys

import svtplay

ID_LIST_MAIN = 0
ID_LIST_TITLE = 1
ID_WINDOW_TITLE = 2

def Play(url):
	print "pc.Play", url

	os.system("gnome-www-browser %s" % url)


def SetListItems(list_id, new_items):
	print "pc.SetListItems"

	i = 0
	for item in new_items:
		print i, item
		i += 1

def ActivateWindow(win_id):
	svtplay.OnUnLoad()
	svtplay.OnLoad()

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

		if input == "back":
			svtplay.OnUnLoad()
			svtplay.OnLoad()
			continue

		try:
			svtplay.OnClick(int(input))
		except TypeError as e:
			print e


if __name__ == "__main__":
	print "main"
	svtplay.OnLoad()
	run()
