#!/usr/bin/python3

import urllib.parse
import urllib.request
import json
from datetime import datetime
import sys
import os.path
import time
import crcmod
import requests
import locale
from base64 import b64encode
from hashlib import sha256

def get_position(PayloadID):
	url = 'http://spacenear.us/tracker/datanew.php?mode=Position&type=positions&format=json&max_positions=1&vehicles=' + PayloadID
	
	print("Checking payload " + PayloadID)
	
	req = urllib.request.Request(url)
	try:
		with urllib.request.urlopen(req) as response:
			result = response.read()			# content = urllib.request.urlopen(url=url, data=data).read()
	except Exception as e:
		print ("Failed to download")
		return None

	# print(result)
	
	result = result.decode('utf-8')
	
	j = json.loads(result)
	
	positions = j['positions']['position']
	
	if len(positions) > 0:
		return positions[0]
		
	return None


def UploadTelemetry(Callsign, Sentence):
	sentence_b64 = b64encode(Sentence.encode())

	date = datetime.utcnow().isoformat("T") + "Z"
	
	data = {"type": "payload_telemetry", "data": {"_raw": sentence_b64.decode()}, "receivers": {Callsign: {"time_created": date, "time_uploaded": date,},},}
	data = json.dumps(data)
	
	url = "http://habitat.habhub.org/habitat/_design/payload_telemetry/_update/add_listener/%s" % sha256(sentence_b64).hexdigest()
	req = urllib.request.Request(url)
	req.add_header('Content-Type', 'application/json')
	try:
		response = urllib.request.urlopen(req, data.encode())
		print ("Uploaded OK")
	except Exception as e:
		print ("Failed to upload")
		pass
		# return (False,"Failed to upload to Habitat: %s" % (str(e)))

def crc16_ccitt(data):
    crc16 = crcmod.predefined.mkCrcFun('crc-ccitt-false')
    return hex(crc16(data))[2:].upper().zfill(4)

def post_position(index, position):
	data = position['data']

	print("data=" + str(data))

	temp = 'XX,' + position['sequence'] + ',' + position['gps_time'].split(' ')[1] + ','
	
	if 'pred_lat' in data:
		temp = temp + data['pred_lat'] + ',' + data['pred_long'] + ',145'
	else:
		temp = temp + data['predicted_latitude'] + ',' + data['predicted_longitude'] + ',145'
	
	sentence = '$$' + temp + '*' + crc16_ccitt(temp.encode()) + '\n'	

	print("sentence: ", sentence)
	
	UploadTelemetry('M0RPI', sentence)
	
	
# Main loop

if len(sys.argv) < 2:
	print("Usage: python xx.py <payload_ID>")
	quit()


PayloadIDs=[]
gps_time=[]

print("Monitoring payload(s):", end="")
PayloadIDs = []
for i in range(1, len(sys.argv)):
	PayloadIDs.append(sys.argv[i])
	
	gps_time.append(None)

	print(' ' + sys.argv[i], end="")
print()

while True:
	for index, PayloadID in enumerate(PayloadIDs):
		position = get_position(PayloadID)
		
		if position:
			if position['gps_time'] != gps_time[index]:
				data = position['data']
				if gps_time[index]:
					print('Got new position at ' + position['gps_time'])

					post_position(index, position)
					
				gps_time[index] = position['gps_time']
			
		time.sleep(10)

