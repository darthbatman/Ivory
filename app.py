import subprocess
import time
import os

fileName = time.strftime("%c").replace(" ", "").replace(":", "")

togetherRecordCommand = "raspivid -c -o " + fileName + ".h264 -k -t 15000 -b 5000000 | arecord --device=hw:1,0 --format S16_LE --rate 44100 -c1 " + fileName + ".wav -V mono"
camRec = subprocess.Popen(("raspivid -c -o " + fileName + ".h264 -k -t 15000 -b 5000000").split(), stdout=subprocess.PIPE)
micRec = subprocess.Popen(("arecord --device=hw:1,0 --format S16_LE --rate 44100 -c1 " + fileName + ".wav -V mono").split(), stdout=subprocess.PIPE)
camRec.wait()
micRec.wait()

getDurationCommand = "ffprobe -i " + fileName + ".wav -show_entries format=duration -v quiet -of csv=\"p=0\""
process = subprocess.Popen(getDurationCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

duration = int(float(output))

trimAudioCommand = "ffmpeg -ss " + str(duration - 15) + " -t " + str(duration) + " -i " + fileName + ".wav " + fileName + "1.wav"
process = subprocess.Popen(trimAudioCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

##h264ToMP4Command = "MP4Box -fps 30 -add " + fileName + ".h264 " + fileName + ".mp4"
##process = subprocess.Popen(h264ToMP4Command.split(), stdout=subprocess.PIPE)
##output, error = process.communicate()

##recordAudioCommand = "arecord --device=hw:1,0 --format S16_LE --rate 44100 -c1 " + fileName + ".wav -V mono"
##process = subprocess.Popen(recordAudioCommand.split(), stdout=subprocess.PIPE)
##output, error = process.communicate()

##playVideoCommand = "omxplayer -o hdmi " + time.strftime("%c").replace(" ", "").replace(":", "") + ".mp4"
##ffmpegConcatenateCommand = "ffmpeg -i SatJan210322022017.mp4 -i SatJan210322052017.mp4 -filter_complex concat=n=2:v=1:a=0 -f MOV -vn -y output.mp4"
##circularBufferCommand = "raspivid -c -o " + fileName + ".h264 -k -t 15000 -b 5000000"
##
##process = subprocess.Popen(circularBufferCommand.split(), stdout=subprocess.PIPE)
##output, error = process.communicate()
##
##h264ToMP4Command = "MP4Box -fps 30 -add " + fileName + ".h264 " + fileName + ".mp4"
##process = subprocess.Popen(h264ToMP4Command.split(), stdout=subprocess.PIPE)
##output, error = process.communicate()

##getDurationCommand = "ffprobe -i " + fileName + ".wav -show_entries format=duration -v quiet -of csv=\"p=0\""
##process = subprocess.Popen(getDurationCommand.split(), stdout=subprocess.PIPE)
##output, error = process.communicate()
##
##duration = int(float(output))
##
##trimAudioCommand = "ffmpeg -ss " + str(duration - 15) + " -t " + str(duration) + " -i " + fileName + ".wav " + fileName + "1.wav"
##process = subprocess.Popen(trimAudioCommand.split(), stdout=subprocess.PIPE)
##output, error = process.communicate()

##counter = 0
##
##while counter <= 20:
##    recordVideoCommand = "raspivid -o " + time.strftime("%c").replace(" ", "").replace(":", "") + ".h264 -t 1000"
##    process = subprocess.Popen(recordVideoCommand.split(), stdout=subprocess.PIPE)
##    output, error = process.communicate()
##    print(counter)
##    if counter >= 15:
##        #delete earliest h264 file
##        minimum = 9999999999.00
##        earliestFile = ""
##        earlyFile = False
##        for file in os.listdir(os.path.dirname(os.path.realpath(__file__))):
##            earlyFile = False
##            if file.endswith(".h264"):
##                if os.path.getmtime(file) < minimum:
##                    minimum = os.path.getmtime(file)
##                    earliestFile = file
##                    earlyFile = True
##        if earlyFile is True:
##            os.remove(file)
##            print(file)
##    counter += 1
##
##counter = 0
##
##while counter < 15:
##    for file in os.listdir(os.path.dirname(os.path.realpath(__file__))):
##            earlyFile = False
##            if file.endswith(".h264"):
##                h264ToMP4Command = "MP4Box -fps 30 -add " + file.replace(".h264", "") + ".h264 " + file.replace(".h264", "") + ".mp4"
##                process = subprocess.Popen(h264ToMP4Command.split(), stdout=subprocess.PIPE)

##recordAudioCommand = "arecord -D plughw:1,0 -f dat -d 4 " + time.strftime("%c").replace(" ", "").replace(":", "") + ".wav"
##process = subprocess.call(recordAudioCommand.split(), stdout=subprocess.PIPE)
