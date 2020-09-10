#!/usr/bin/env python3
from subprocess import check_output
import os
from multiprocessing import Pool
from datetime import datetime
# username = 'admin'
# password = 'admin123'
# dvr_ip = '192.168.0.104'

# link = 'rtsp://' + username + ':' + password+'@' + dvr_ip + ":554/Streaming/Channels/101"
# link2 = 'rtsp://admin:admin%40123@192.168.0.200:554/Streaming/Channels/101'

## checks if the folder / location exists or not
def check_location(name):
	location=os.path.join(os.getcwd(),'hls',name, str(datetime.now()).split(' ')[0])
	if not os.path.exists(location):
		try:
			#os.mkdir(os.path.join("static",str(datetime.now()).split(" ")[0]))
			os.makedirs(location)
			return location
		except:
			os.makedirs(location)
			return location


def get_segments(args):
	dvr_ip, channel, username, password, mode, name = args

	located=check_location(name)
	print(located)
	if channel == '':
		source="rtsp://"+username+':'+password+'@'+dvr_ip
	else:
		source="rtsp://" + username + ':' + password + '@' + dvr_ip + ":554/Streaming/Channels/"+ channel
	#check_location(location, name)
	# if os.path.exists(location+'\\index.m3u8'):
	# 	with open(location+'\\index.m3u8', "r") as frames_file:
	# 		data = frames_file.readlines()
	# 		start_index = int(data[-1].split('.')[0]) +1
	# 		if type(data[-1].split('.')[0]) == int:
	# 			print('integer type')
	# 		else:
	# 			print('not an integer')
	# else:
	# 	start_index = 1
	# print(start_index)
	# -loglevel panic 
	os.system("ffmpeg -loglevel panic -fflags nobuffer  -rtsp_transport tcp  -i "+source+
			" -vsync 0  -copyts  -vcodec copy  -movflags frag_keyframe+empty_moov  -an  -hls_flags"
			" delete_segments+append_list  -f segment  -segment_list_flags live  -segment_time 10"
	    	"  -segment_list_size 20  -segment_format mpegts  -segment_list "+located+"/index.m3u8 -segment_list_type"
	    	" m3u8 "+located+"/%d.ts")


def get_from_file():
	dvrIP = []
	channel = []
	mode = []
	username = []
	password = []
	name=[]
	with open(os.path.join(os.getcwd(),"office_cam.txt"),"r") as file: 
		data = file.readlines()
		print(data)

	for i in range(len(data)):
		#d=(data[i].split(":")[-1])
		data[i] = data[i].split(' : ')
		dvrIP.append(data[i][0])
		channel.append(data[i][1])
		username.append(data[i][2])
		password.append(data[i][3])
		mode.append(data[i][4])
		name.append(data[i][5].split("\n")[0])
		#vidtime.append(data[i][6])
		## inserting into database
		#insertCameraHealth(data[i][5],data[i][0])


		#print("asss",data[i][6])
		## checks daily or an entry
		#if checkout():
		#	dailyEntry(data[i][5].split("\n")[0],datetime.now(),data[i][0])

	print("Running on {} Cameras".format(len(data)))
	pool = Pool(len(data))
	pool.map(get_segments, zip(dvrIP, channel, username, password, mode, name))

if __name__== '__main__':
	get_from_file()

# python IdeaProjects\FLIPKART\livestream_pool.py
