# FIXME: use ConfigParser or similar tool to actually read (and write?) config values

defaults = {
		"host" : "192.168.0.103",
		"port" : 9001
		}

def get(key):
	# FIXME: consult parsed config file
	return defaults[key]
