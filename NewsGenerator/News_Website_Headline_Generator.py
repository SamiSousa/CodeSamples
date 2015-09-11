'''
Sami Shahin
May 6 2015
News Site Headline Seeker
Finds headlines for news sites (works for CNN and BBC)
Using two functions, creates a .txt file of those headlines, as well as returning said headlines
'''
#//Adding additional comments for a walkthrough of what my code does. The additional comments will be prefaced with '#//'
#// Uses re, urllib, codecs, and bs4 libraries

import re 	#//regular expression library; for finding paterns in the html
from bs4 import BeautifulSoup	#//using BeautifulSoup to easily take apart the website html
import urllib.request 	#//reading website
import urllib.error 	#//for when urllib gives an error
import codecs 	#//used in reading and writing .txt files; html isn't implicitly in utf-8 (bbc uses foreign languages for alternate sites)

def headlineSearch(url):
	#takes a url as a string, and returns a list of headlines
	#must be for cnn; will inspect other news sites
	#uses bs4, urllib.request, and re libraries
	try:
		website =  urllib.request.urlopen(url).read() 	#//reads website html
	except urllib.error.URLError as e: 		#//in the case that there is an error
		if hasattr(e, 'reason'):
			print("We failed to reach a server.")
			print('Reason: ', e.reason)
		elif hasattr(e, 'code'):
			print("The server couldn't fulfill the request.")
			print("Error code: ", e.code)
	else:
		websoup = BeautifulSoup(website) 	#creates BeautifulSoup object of website, for easy manipulation

		headlines = [] 	#empty list, for holding headlines
		splitter = "" 	#//holds string element for splitting
		regcheck = r'' 	#//holds regular expression to be compared to in search
		if url == "http://www.cnn.com/":
			splitter = ',' 		#//cnn's website uses lots of commas in it's html, and I found it convenient to split the html at these points
			regcheck = r'"headline":"(.*)"'
		else:
			splitter = '>' 		#//all websites' html has angle brackets, and end brackets are a very convenient place to split the string
			regcheck = r'title="(.*)"'
		for child in websoup.body.children:	#for every child of the <body> tag
			split = str(child).split(splitter)	#split the child by the splitter character
			for part in split:	#for every partition of split
				headSeek = re.search(regcheck,str(part), re.X) 	#search match to '"headline":' in partition (or 'title=' in bbc's case)
				if headSeek:	#if successful
					if "Newsroom" in headSeek.group(1): 	#//for bbc: after the title is Newsroom, the results aren't actually headlines, so I stop the search there. Strangely enough, it was "Newsday" before, so they might be changing their html frequently
						break
					headlines.append(headSeek.group(1))	#append headline to list
		if url == "http://www.bbc.com/": 	#//in the case the url searched is BBC
			del(headlines[0])		#first line of bbc's titles is "British Broadcasting Corporation"
		return headlines 		#//returns the result of the search, which should be a list of headline strings


def writeHeadline(url, filename="headlines.txt",op='w'):
	#takes a url as a string, writes a file of the headlines from the website
	#takes optional argument for filename and op; if op set to "r+", will add to a current file named filename
	#works for cnn, let's try other news websites
	#uses bs4, urllib.request, and re libraries
	try:
		with codecs.open(filename, op, 'utf-8') as headtxt:
			search = headlineSearch(url) 	#//runs the function above, which searches for headlines from the url
			if search:
				for head in headlineSearch(url):
					headtxt.write(head)
					headtxt.write('\r\n')	#odd that I need to use '\r\n' for bbc, but not cnn. maybe something about codecs...
				return search
			else:
				return None
	except OSError as e: 	#// in the case the file cannot be found or other file error, such as in the case of op="r+" before the file is created
		print('Error number: ', e.errno)

cnnurl ="http://www.cnn.com/"
writeHeadline(cnnurl, "cnn_headlines.txt")

foxurl = "http://www.foxnews.com/"
#writeHeadline(foxurl, "fox_headlines.txt")
#gives error; 404
#// for some reason it cannot find fox news's website; will look into this further

bbcurl = "http://www.bbc.com/"
writeHeadline(bbcurl, "bbc_headlines.txt")
