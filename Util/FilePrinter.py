from bs4 import BeautifulSoup
import requests
import random
import re

def Status():
	r = requests.get("http://limitlessmc.net/")
	soup = BeautifulSoup(r.text, "html.parser")
	val = soup.select("#serverstatus")
	return val[0].text

def wotd():
	packet = {}
	r = requests.get("https://www.merriam-webster.com/word-of-the-day")
	soup = BeautifulSoup(r.text, "html.parser")
	val = soup.select("div")
	soup = BeautifulSoup(str(val[44]), "html.parser")
	val = soup.select("span")
	packet['Day'] = val[0].text[11:]

def ForumPost(url : str, num = 0):
	r = requests.get(url)
	soup = BeautifulSoup(r.text, "html.parser")
	Side = soup.select("div.pull-left")
	val = soup.select("div.content")

	#mainclean = val[0].text

	text = str(val[num]).split('<br/>')
	text[num] = text[num].replace('<div class="content">', '')
	text[len(text)-1] = text[len(text)-1].replace('</div>', '')
	nText = []
	for l in text:
		nText.append(cleanLine(l))
	mainclean = '\n'.join(nText)


	clean = "**" + Side[2].text.replace("\n", '') + "**" + Side[3].text.replace('\t', '') + "------------------------------------" + "\n" + mainclean
	if(len(clean) > 1500):
		clean = clean[:1450] + "...\n------------------------------------\n*If you would like to read more, click the link below!*\n{}".format(url)


	#print(clean)
	return clean

def fmlText():
	r = requests.get("http://www.fmylife.com/random")
	soup = BeautifulSoup(r.text, "html.parser")
	val = soup.select("p.content")
	if(len(val) < 1):
		print("ERROR in FML cmd")
		r = requests.get("http://www.fmylife.com/random")
		soup = BeautifulSoup(r.text, "html.parser")
		val = soup.select("p.content")
	return val[0].text

def cleanLine(line):
	print('cleaning')
	#print(line)
	if('<span style="font-weight: bold">' in line):
		line = line.replace('<span style="font-weight: bold">', '**')
		line = line.replace('</span>', '**')
		line.replace("\n", '')
		#line = "**" + line + "**\n"
	line = line.replace('<img alt=";)" src="./images/smilies/icon_e_wink.gif" title="Wink"/>', ';)')
	line = line.replace('<img alt=":(" src="./images/smilies/icon_e_sad.gif" title="Sad"/>', ':(')



	if('<a class="postlink" href="' in line):
		line = line.replace('<a class="postlink" href="', '')
		line = line.replace('</a>', '')
	#print(line)
	return line

def youtube(input1:str, num = 0):
	r = requests.get("https://www.youtube.com/results?search_query="+input1)
	soup = BeautifulSoup(r.text, "html.parser")
	val = soup.select("h3")
	m = re.search('href="/watch\?v=(.{11})"', str(val[4 + num]))
	#print(str(val[4 + num]), '\n')
	#print(m.group(0)[15:-1])
	if(m == None):
		return youtube(input1, num+1)
	return 'https://www.youtube.com/watch?v=' + m.group(0)[15:-1]

def nextSong(url, num = 0):
	r = requests.get(url)
	soup = BeautifulSoup(r.text, "html.parser")
	val = soup.select("a")
	m = re.search('href="/watch\?v=(.{11})"', str(val[20 + num]))
	if(m == None):
		return nextSong(url, num+1)
	return 'https://www.youtube.com/watch?v=' + m.group(0)[15:-1]

def wouldYouRather():
	r = requests.get("http://either.io/")
	soup = BeautifulSoup(r.text, "html.parser")
	val = soup.select("span")
	return [(val[6].text, val[11].text) , (val[7].text, val[15].text)]



# r = requests.get("https://www.merriam-webster.com/word-of-the-day")
# soup = BeautifulSoup(r.text, "html.parser")
# val = soup.select("div")
# #print(val[44])
# soup = BeautifulSoup(str(val[44]), "html.parser")
# val = soup.select("span")
# # #print(val[20])
# # m = re.search('href="/watch\?v=(.{11})"', str(val[20]))
# # print('https://www.youtube.com/watch?v=' + m.group(0)[15:-1])
# # count = 0
# # for v in val:
# # 	if count < 20:
# # 		try:
# # 			print(str(count), v.text)
# # 		except Exception as e:
# # 			print(e, "Error")
# # 	count += 1

# print(val[0].text[11:])

# packet = {}
# r = requests.get("https://www.merriam-webster.com/word-of-the-day")
# soup = BeautifulSoup(r.text, "html.parser")
# val = soup.select("div")

# soup2 = BeautifulSoup(str(val[44]), "html.parser")
# val2 = soup2.select("span")
# packet['Day'] = val2[0].text[11:-8]

# val3 = soup2.select("div")
# packet['Word'] = val3[4].text[1:-7]

# val4 = soup.select("p")
# packet['Defintion = ']
# count = 0
# for v in val4:
# 	if count < 20:
# 		try:
# 			print(str(count), v.text)
# 		except Exception as e:
# 			print(e, "Error")
# 	count += 1


# r = requests.get("http://either.io/")
# soup = BeautifulSoup(r.text, "html.parser")
# val = soup.select("span")
# count = 0
# for v in val:
# 	if count < 20:
# 		try:
# 			print(str(count), v.text)
# 		except Exception as e:
# 			print(e, "Error")
# 	count += 1

# print(val[6].text, val[11].text)
# print(val[7].text, val[15].text)


# for x in val3:
# 	print(x.text)
#print(val3)
#print(packet)


# print(val.text)
# while val[num].text == "Cacophony":
# 	num =+ 1
# 	try:
# 		print(val[num].text)
# 	except Exception:
# 		print("ERROR")

# f = open(val[23].text.strip(), 'r')
# print(f.read())




########### Getting Pictures #########################
# r = requests.get("http://pokemondb.net/pokedex/national")
# soup = BeautifulSoup(r.text, "html.parser")
# val = soup.select(".infocard-tall")



# name = "Venusaur"

# #print(val[ID(name) - 1]['class'])
# val2 = val[ID(name) - 1].select("a")
# count = 0
# print(val2[0]["data-sprite"])