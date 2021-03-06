"""
PyAudio example: Record a few seconds of audio and save to a WAVE
file.
"""

import pyaudio
import wave
import sys
import os
import time
from kivy.core.audio import SoundLoader

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5

def record(filename):
	#if sys.platform == 'darwin':
	#	CHANNELS = 1

	p = pyaudio.PyAudio()

	# Would be nice to play a little sound here - a beep or something - to indicate that recording has begun
	#sound = SoundLoader.load('./beep1.wav')
	#sound.play()
	

	stream = p.open(format=FORMAT,
    	            channels=CHANNELS,
        	        rate=RATE,
            	    input=True,
                	frames_per_buffer=CHUNK)

	print("* recording")

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)

	print("* finished recording")
	#sound = SoundLoader.load('./beep1.wav')
	#sound.play()

	stream.stop_stream()
	stream.close()
	p.terminate()

	os.chdir('../recordings/')
	wf = wave.open(filename + '.wav', 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()