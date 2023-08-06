import os
import sys
import time
import yaml
import urllib
import tempfile
import requests
import platform
import urllib.request as req

TEMP = tempfile.gettempdir()
arch = platform.architecture()[0]
progress = ["|","/","-","\\"]

def clear():
	command = 'clear'
	if os.name in ('nt', 'dos'):
		command = 'cls'
	os.system(command)

def download(names):	
	names = list(names)
	for name in names:
		if "(" and ")" not in name:
			ver = "latest"
		else:
			ver = name[name.find("(")+len("("):name.find(")")]
			name_ver_r = name.replace("({})".format(ver),"")
		num = 0
		start = time.time()
		print("Looking for file links..", end = "\r")
		try:
			try:
				file_info = req.urlopen("https://proget.whirlpool.repl.co/data/{}.yml".format(name_ver_r))
			except urllib.error.HTTPError:
				print("cannot find file information of {}".format(name))
				continue
		except urllib.error.URLError:
			print("Unable to connect... Check your connection..")
			continue
		url_contents = file_info.read().decode()
		url_data = yaml.safe_load(url_contents)
		data = url_data
		#url_contents = url_contents.split("\n")
		if data[name_ver_r][ver][arch]["installer"][0][0] != "~":
			url = data[name_ver_r][ver][arch]["installer"][0]
		else:
			url = data[name_ver_r][ver][arch]["installer"][0][2:-1]
			print(url)
			continue
		#url = url_contents[0].split("~")[-1]
		local_filename = TEMP+"\\"+url.split('/')[-1]
		print("Reaching requested file..", end = "\r")
		url_file = req.urlopen(url)
		size= url_file.headers["Content-Length"]	
		print("Starting to download file", end = "\r")
		with requests.get(url, stream=True) as r:
			r.raise_for_status()
			with open(local_filename, 'wb') as f:
				sz = 0
				for chunk in r.iter_content(chunk_size=8192):  
					percent = sz / int(size)*100
					f.write(chunk)
					sz = sz+8192
					#print("abc ",floor_percent, sz)
					print("Downloading.. [{}] file \"{}\" Done: {}%  of {}kb".format(progress[num], url, round(percent,2),int(size)/1024), end = "\r")
					if num != 3:num = num+1
					else: num = 0
	
		print("Finished in {} seconds".format(time.time()-start))
		#print("file can be found at {}".format(local_filename))
		os.system(local_filename)
		return local_filename

if __name__ in "__main__":  
	if "download" in sys.argv[1].lower():
		download(sys.argv[2:])
	elif "uninstall" in sys.argv[1].lower():
		print("Uninstaller coming soon..")
	else:
		print('Unknown option "{}"'.format(sys.argv[1]))