import time
import BaseHTTPServer
import subprocess
import os
import time
import wave
import contextlib
import re
from subprocess import Popen, PIPE
import requests
import json

apiKey = '190b06c919f95da69f6c491f7d54673f'

global httpd

def upvoteMemory():

	url = 'http://api.reimaginebanking.com/accounts/588466671756fc834d8fb0e7/deposits?key=190b06c919f95da69f6c491f7d54673f'
	payload = {
		"medium": "balance",
		"transaction_date": "2017-01-22",
		"amount": 20,
		"description": "string"
		}
# Send the POST request
	response_eight = requests.post( 
		url, 
		data=json.dumps(payload),
		headers={'content-type':'application/json'},
		)
	b = json.loads(response_one.text)
	c = json.loads(response_eight.text)
	d = (b["objectCreated"]["balance"]) + int(c["objectCreated"]["amount"])
	if response_eight.status_code == 201:
		print "Awesome memory, Jane has been awarded twenty points for memory that many people around the world like!"
		print "Jane's Balance:" + str(d)

def memoryShare():
	url = 'http://api.reimaginebanking.com/accounts/{}/withdrawals?key={}'.format(customerId_Jane_Account,apiKey)
	payload = {
	 	"medium": "balance",
	  	"transaction_date": "2017-01-22",
	  	"amount": "10",
	  	"description": "string"
	}
	# Send the POST request
	response_seven = requests.post( 
		url, 
		data=json.dumps(payload),
		headers={'content-type':'application/json'},
	)
	b = json.loads(response_one.text)
	c = json.loads(response_seven.text)
	d = (b["objectCreated"]["balance"]) - int(c["objectCreated"]["amount"])
	if response_seven.status_code == 201:
		print('Jane has shared a memory!')
		print("Jane Doe's Balance:" + str(d))

def keypress(sequence):
    p = Popen(['xte'], stdin=PIPE)
    p.communicate(input=sequence)

fileName = time.strftime("%c").replace(" ", "").replace(":", "")

camRec = subprocess.Popen(("raspivid -rot 90 -c -o " + fileName + ".h264 -k -t 15000 -b 5000000").split(), stdout=subprocess.PIPE)
micRec = subprocess.Popen(("arecord --device=hw:1,0 --format S16_LE --rate 44100 -c1 " + fileName + ".wav -V mono").split(), stdout=subprocess.PIPE)

HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9000 # Maybe set this to 9000.


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Title goes here.</title></head>")
        s.wfile.write("<body><p>This is a test.</p>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        s.wfile.write("</body></html>")
        if (s.path == "/share"):
            print("MEMORY SHARED")
            memoryShare()
        if (s.path == "/up"):
            print("MEMORY UPVOTED")
            upvoteMemory()
        if (s.path == "/end"):
            print("END RECORDING!")
            
            control_f4_sequence = '''key Return
            '''

            keypress(control_f4_sequence)
            micRec.kill()
            process = subprocess.Popen(['ffmpeg',  '-i', fileName + ".wav"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = process.communicate()
            matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()

            duration = int(float(matches['seconds']))

            trimAudioCommand = "ffmpeg -ss " + str(duration - 15) + " -t " + str(duration) + " -i " + fileName + ".wav " + fileName + "1.wav -y"
            process = subprocess.Popen(trimAudioCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            combineAVCommand = "ffmpeg -i " + fileName + "1.wav -i " + fileName + ".h264 -vcodec copy video.mp4"
            process = subprocess.Popen(combineAVCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            httpd.server_close()

            fileServerCommand = "python -m SimpleHTTPServer 9000"
            process = subprocess.Popen(fileServerCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()   

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
