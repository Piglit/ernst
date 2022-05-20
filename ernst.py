
import subprocess
import re
import sys

DEFAULTPITCH = 5
PITCHFACTOR = 5

def say(text, pitch=DEFAULTPITCH):
	cmd = ['echo', 'p', str(pitch), f'"{text}"']
	subprocess.run(cmd)

def test_say():
	say("das ist ein Test")
	say("noch ein Test", pitch=10)

def splitStars(text):
	entries = re.split(r'\s*(\%+)\s*(\w+)\s*', text)
	entries = [e for e in entries if e]	# removes empty strings
	#print(entries)
	return entries

def test_splitStars():
	splitStars("kein Eintrag")
	splitStars("ein % Eintrag")
	splitStars("% zwei % Einträge")
	splitStars("%%% multiple Einträge")
	splitStars("Fehler % ")
	splitStars(" % ")
	splitStars("%ich%provoziere")
	splitStars("%ich%provoziere % % ungültig")

def dispatch(text):
	entries = splitStars(text)
	pitch = None
	for e in entries:
		if e.startswith("%"):
			pitch = len(e)	# amount of next pitch
		elif pitch:
			say(e, pitch=DEFAULTPITCH+pitch*PITCHFACTOR)
			pitch = None	# reset pitch to default
		else:
			say(e)			# default pitch it is

def test_splitStars():
	dispatch("kein Eintrag")
	dispatch("ein % Eintrag")
	dispatch("% zwei % Einträge")
	dispatch("%%% multiple Einträge")
	dispatch("Fehler % ")
	dispatch(" % ")
	dispatch("%ich%provoziere")
	dispatch("%ich%provoziere % % ungültig")


if __name__ == "__main__":
	text = " ".join(sys.argv[1:])
	dispatch(text)
