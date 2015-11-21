import os
import os.path
import random
from Color import Color

showsPath = "./Text Files/"
watchedFile = showsPath + "watched.txt"
movieKey = 'M'
seriesKey = 'S'
netflixNetwork = "Netflix"
hboNetwork = "HBO"
torrentNetwork = "BitTorrent/CouchTuner/Some Knock Off Site"
theaterNetwork = "Theater"
noShows = []

def combineDicts(dictObj1, dictObj2):
	finalDictObj = dict()
	for key in dictObj1:
		finalDictObj.update({key : dictObj1[key]})
	for key in dictObj2:
		if key not in finalDictObj:
			finalDictObj.update({key : dictObj2[key]})
	return finalDictObj

def handleInput(inputStr):
	inputStr += " (y/n): "
	resp = raw_input(inputStr).lower()
	while resp != 'y' and resp != 'n':
		resp = raw_input(inputStr).lower()
	return resp

def insertShows(fileList, showList):
	for f in fileList:
		with open(f, 'r') as showFile:
			showKey = movieKey if 'movie' in f.lower() else seriesKey
			for l in showFile.readlines():
				showList.update({ l.strip() : showKey })

def watchedShow(show, networkShows, network):
	preName = network.lower()
	if network == torrentNetwork:
		preName = 'torrent'
	postName = ""
	if networkShows[show] == movieKey:
		postName = "movies"
	elif networkShows[show] == seriesKey:
		postName = "series"

	with open(watchedFile, 'a') as wFile:
		wFile.write(show + '\n')

	showFileName = "{0}{1}_{2}.txt".format(showsPath, preName, postName)
	with open(showFileName, 'r') as sFile:
		showList = [ l.strip() for l in sFile.readlines() ]

	showList = set(showList) - set([show])
	with open(showFileName, 'w') as sFile:
		for s in showList:
			sFile.write(s.strip() + '\n')

	del networkShows[show]

def makeSelection(shows, netflixShows, hboShows, torrentShows, theaterShows):
	global noShows
	if len(noShows) == len(shows.keys()):
		print "{0}You have said you do not want to watch any of the listed shows. " \
				"Resetting lists, please update your show lists and re-run this program.{1}\n".format(Color.YELLOW, Color.END)
		noShows = []
	show = random.choice(shows.keys())
	while show in noShows:
		show = random.choice(shows.keys())
	network = ""
	networkShows = None
	color = Color.PURPLE
	middle = "on"
	if show in netflixShows:
		network = netflixNetwork
		networkShows = netflixShows
		color = Color.RED
	elif show in hboShows:
		network = hboNetwork
		networkShows = hboShows
		color = Color.CYAN
	elif show in torrentShows:
		network = torrentNetwork
		networkShows = torrentShows
		color = Color.PURPLE
	elif show in theaterShows:
		network = theaterNetwork
		networkShows = theaterShows
		color = Color.BLUE_HIGHLIGHT
		middle = "in"
	return "{0}{1}{2} {3} {4}{5}{6}".format(Color.UNDERLINE, show, Color.END, middle, color, network, Color.END), show, networkShows, network

def chooseShow(netflixShows, hboShows, torrentShows, theaterShows):
	global noShows
	shows = combineDicts(netflixShows, hboShows)
	shows = combineDicts(shows, torrentShows)
	shows = combineDicts(shows, theaterShows)
	firstShow = True
	while True:
 		showPrint, show, networkShows, network = makeSelection(shows, netflixShows, hboShows, torrentShows, theaterShows)
		resp = handleInput("Do you want to watch: {0}?".format(showPrint))
		if resp == 'y':
			raw_input("Press any key when you are done with {0}{1}{2}: ".format(Color.UNDERLINE, show, Color.END))
			firstShow = False
			noShows = []
			if networkShows[show] == movieKey:
				watchedShow(show, networkShows, network)
			else:
				if handleInput("Are you done with this series?") == "y":
					watchedShow(show, networkShows, network)
		else:
			noShows.append(show)
		if not firstShow and handleInput("Are you done watching shows?") == 'y':
			break
		elif not firstShow:
			firstShow = True
		print "\n"

def main():
	netflixShows = dict()
	hboShows = dict()
	torrentShows = dict()
	theaterShows = dict()
	netflixFiles = [showsPath + f for f in os.listdir(showsPath) if os.path.isfile(showsPath + f) and 'netflix' in f]
	hboFiles = [showsPath + f for f in os.listdir(showsPath) if os.path.isfile(showsPath + f) and 'hbo' in f]
	torrentFiles = [showsPath + f for f in os.listdir(showsPath) if os.path.isfile(showsPath + f) and 'torrent' in f]
	theaterFiles = [showsPath + f for f in os.listdir(showsPath) if os.path.isfile(showsPath + f) and 'theater' in f]
	insertShows(netflixFiles, netflixShows)
	insertShows(hboFiles, hboShows)
	insertShows(torrentFiles, torrentShows)
	insertShows(theaterFiles, theaterShows)
	chooseShow(netflixShows, hboShows, torrentShows, theaterShows)

if __name__ == '__main__':
	main()
