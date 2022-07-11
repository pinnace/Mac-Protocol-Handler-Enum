#!/usr/bin/env python3

import os
from pprint import pprint 
import plistlib 
import itertools
import getpass

user = getpass.getuser()
plists = []
for directory in ["/Applications/", "/Users/" + user + "/Library/"]:
	files = os.walk(directory)
	for dirpath,_,afile in files:
		if "Info.plist" in afile:
			plists.append(dirpath + "/Info.plist")

urlschemes = []
for plist in plists:
	try:
		with open(plist,"rb") as f:
			p = plistlib.load(f)
			if "CFBundleURLTypes" in p.keys(): 
				protocol_handler_struct = {}
				protocol_handler_struct["Application"] = {}
				protocol_handler_struct["Application"]["Name"] = p["CFBundleIdentifier"]
				protocol_handler_struct["Application"]["URL Names"] = None
				if len(p["CFBundleURLTypes"]) and "CFBundleURLName" in p["CFBundleURLTypes"][0].keys():
					protocol_handler_struct["Application"]["URL Names"] = [d['CFBundleURLName'] for d in p["CFBundleURLTypes"] if 'CFBundleURLName' in d.keys()]
				protocol_handler_struct["Application"]["URL Schemes"] = list(itertools.chain(*[d['CFBundleURLSchemes'] for d in p["CFBundleURLTypes"] if 'CFBundleURLName' in d.keys()]))
				urlschemes.append(protocol_handler_struct)
	except Exception as e:
		print("Error:" + str(e))
	
pprint(urlschemes)
