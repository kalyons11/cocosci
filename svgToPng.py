from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from os import listdir
from os.path import isfile, join

def svgToPng():
	mypath = "C:\\Users\\luke2\\Dropbox (MIT)\\MIT Bibles\\6\\6.804\\Final Project\\cocosci\\test\\" #len 75
	topFolders = [f for f in listdir(mypath)]

	folders = []

	for f in topFolders:
		if f == "LeagueMinutes_12_16_18_mem":
			for folder in listdir(mypath + f):
				folders.append(mypath + f + '\\' + folder)


	for path in folders:
		onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
		for file in onlyfiles:
			if ".svg" in file:
				drawing = svg2rlg(path + "\\" + file)
				renderPM.drawToFile(drawing, path + "\\" + file[:-4] + ".png", fmt="PNG")
				
if __name__ == "__main__":
	svgToPng()