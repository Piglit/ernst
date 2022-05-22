#!/usr/bin/env python3
import subprocess
import re
from os import path
import sys
from time import sleep

DEFAULTPITCH = 5
PITCHFACTOR = 5

SPEAKERS = {
	"elsn":		["-v", "mb-de1", "-g", "10", "-s", "160", "-z", (50,15)],
	"bernd":	["-v", "mb-de2", "-g", "8", "-s", "170", "-z", (50,10)],
#	"clara":	["-v", "mb-de3", "-g", "5",  "-s", "145", "-z", (10,15)],
#	"dieter":	["-v", "mb-de4", "-g", "10", "-s", "170", "-z", (50,10)],
	"steffi":	["-v", "mb-de5", "-g", "8",  "-s", "150", "-z", (55,15)],
	"fred":		["-v", "mb-de6", "-g", "8",  "-s", "140", "-z", (45,12)],
	"gudrun":	["-v", "mb-de7", "-g", "5",  "-s", "150", "-z", (30,15)],
	"ernst":	["-v", "mb-de8", "-g", "15", "-s", "125", "-z", (5,15)]	# do not install mbrola-de8
		}


def say(text, speaker, pitch=0):
	speakerParams = SPEAKERS[speaker][:-1]
	pitchBase, pitchFactor = SPEAKERS[speaker][-1]
	cmd = ["espeak"] + speakerParams + ["-p", str(pitchBase+pitchFactor*pitch), f'"{text}"'] #'-f ankunft'
	print(cmd)
	subprocess.run(cmd)

def _test_say():
	say("das ist ein Test")
	say("noch ein Test", pitch=10)

def splitStars(text):
	entries = re.split(r'\s*(\%+)\s*(\w+)\s*', text)
	entries = [e for e in entries if e]	# removes empty strings
	result = []
	for e in entries:
		result += e.split("\n")
	#print(result)
	return result 

def _test_splitStars():
	splitStars("kein Eintrag")
	splitStars("ein % Eintrag")
	splitStars("% zwei % Einträge")
	splitStars("%%% multiple Einträge")
	splitStars("Fehler % ")
	splitStars(" % ")
	splitStars("%ich%provoziere")
	splitStars("%ich%provoziere % % ungültig")

def dispatch(text, speaker):
	entries = splitStars(text)
	pitch = None
	for e in entries:
		if not e:
			print("pause")
			sleep(0.8)
		elif e.startswith("%"):
			pitch = len(e)	# amount of next pitch
		elif pitch:
			say(e, speaker, pitch=pitch)
			pitch = None	# reset pitch to default
		else:
			say(e, speaker)	# default pitch it is

def _test_splitStars():
	dispatch("kein Eintrag")
	dispatch("ein % Eintrag")
	dispatch("% zwei % Einträge")
	dispatch("%%% multiple Einträge")
	dispatch("Fehler % ")
	dispatch(" % ")
	dispatch("%ich%provoziere")
	dispatch("%ich%provoziere % % ungültig")

def test_speakers():
	text = """
	Guten Morgen Crew.
	Ankunft im Warkien-System steht bevor.
	Macht euch bereit.

	Verlassen des Hyperraums in 3.
	2.
	1.

	% Hüllenbruch
	%% Hüllenbruch
	%%% Hüllenbruch

	Offizierin % Männy auf die Brücke.
	"""

	for speaker in SPEAKERS:
		dispatch(text, speaker)

if __name__ == "__main__":
	#test_speakers()
	#exit(0)
	speaker = sys.argv[0]
	speaker = path.basename(path.normpath(speaker))
	speaker = speaker.removesuffix(".py")
	if speaker not in SPEAKERS:
		raise KeyError(speaker +" not in speakers. Possible speakers are: "+ str([key for key in SPEAKERS.keys()]))
	
	if sys.argv[1] == "-f":
		with open(sys.argv[2], "r") as file:
			text = file.read()
	else:
		text = " ".join(sys.argv[1:])
	dispatch(text, speaker)

