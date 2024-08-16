import time
import os
import re
import pyperclip
import pynput
import codecs
import traceback
import sys
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from pynput.keyboard import Key, Controller
from pynput import keyboard
from inspect import currentframe, getframeinfo
from getpass import getpass
from datetime import datetime
from datetime import date
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import tk
import re
from playwright.sync_api import Page, expect
#import aiofiles as aiof
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor
import requests
import io
from PIL import Image
#Some of this is almost certainly gratuitous. It's a legacy function from when I was using youtube-dl instead of YT-DLP.
#youtube-dl had all sorts of artifacts that appeared in the video's filename which had to be accounted for. YT-DLP does
#not have hear as many, I'm going to comment stuff out, see what happens, and re-add as I run into problems.
def convert_To_Filename(title):				
	video_filename = title
#	while ("://" in video_filename) or (":)" in video_filename) or ("\n" in video_filename) or (":::" in video_filename):
#		print("Modifying filename as variant of title")
#		print(video_filename)
#		video_filename = video_filename.replace(":::", "- - -")
#		video_filename = video_filename.replace("://", " -_")
#		video_filename = video_filename.replace(":)", " -)")
#		video_filename = video_filename.replace("\n", "")
																#I may find other characters that need a similar treatment.
#	while ("*" in video_filename) or ("||" in video_filename) or ("|" in video_filename) or (": " in video_filename) or (":" in video_filename) or ("?" in video_filename) or ('/' in video_filename) or ("__" in video_filename) or ('"' in video_filename) or ('"' in video_filename):
#		video_filename = video_filename.replace("*", "＊") #This part was really wierd. Apparantly it replaces asterisks
															#with underscores UNLESS the asterisk is the final character.
#	video_filename = video_filename.replace('"', '＂')

#		video_filename = video_filename.replace("|", "｜") # I don't have a clue why it would do this since they're both
#	video_filename = video_filename.replace(":", "：")# allowed characters, but ah well.
#		video_filename = video_filename.replace("?", "？") #Apparently the question mark is a reserved character in Windows filenames (DAMN MICROSOFT!)
	video_filename = video_filename.replace('/', '⧸') #so yt-dlp turns it into this not-technically-a-question-mark-character that just
#														 #happens to look like a question mark but is a different symbol so if there's an actual
#		video_filename = video_filename.replace('"', "＂") #question mark in the title we have to convert.
#		video_filename = video_filename.replace('"', "＂") #question mark in the title we have to convert.
	return video_filename


#Likely unnecessary as Playwright has a(n easier) way of handling file uploads. Might delete.
keyboard = Controller()


LOGIN_EMAIL = "BLANK"
LOGIN_PW = "BLANK"
STUFF = "BLANK"
path = "BLANK"
song_file = "BLANK"
video_start = 1
video_end = 1
video_number = 0
Loop_Toggle = 0
line_num = 1
Looking_For_Title = 0
Start_Upload = -1
Look_For_Channel_URL = 0
Look_For_Channel_Name = 0



print("What video do you want to start at?")
video_start = int(input())
while video_start == -1:
	time.sleep(0.5)

print("What video do you want to end at? If you're not sure how many videos there are and want to do them all, just type a super big number that you're reasonably sure is bigger than the playlist size and it will run through them all.")
video_end = int(input())
while video_end == -1:
	time.sleep(0.5)

print("Where is your song playlist file?")
song_file = input()
while song_file == "BLANK":
	time.sleep(0.5)

print("Where will you be saving these, master?")
STUFF = input()
while STUFF == "BLANK":
	time.sleep(0.5)

#Obligatory Playwright boiler plate code. The rest of the program will be performed under here.
with sync_playwright() as p:
	#Open browser
	browser = p.chromium.launch(headless = False)
	page = browser.new_page()
#	page.goto("https://www.youtubethumbnaildownloader.com/")

	songs = codecs.open(str(song_file))

	for line in songs:  # GET THE FILE CONTAINING ALL OUR SONG TITLES + URLS AND SET TO VARIABLES SO WE CAN TYPE THEM IN
		line_num += 1 # Keep track of what line we're on.
		if str("Now playing") in line:
			video_number += 1 # Keep track of what video we're on by using a string that appears once per video.
			if video_number >= video_start and video_number <= video_end: # We want to increase the video number always so we know where we are, but only actually upload if the video number is within specifications.
				print("\n\nnow on video number " + str(video_number) + ":")
				

			#Check the line that appears right above the title. This will be happening most of the time. When we find it, flag Looking_For_Title
		if str('<https://www.youtube.com/watch?v=') in line and str('      <https://www.youtube.com/watch?v=') not in line and Looking_For_Title == 0: # WE'RE PAST THE URL, SO FLAG THE VARIABLE TO START GETTING TITLE
			Looking_For_Title = 1
			title = ("")


			#We're looking for title. This means every line will be added to the title. The first 3 lines after the title are blank so they'll be ignored.
		if Looking_For_Title == 1 and str('<https://www.youtube.com/watch?v=') not in line:
			if line != "\n":
				if title == "":
					title = line
					title = title.partition("      ")[2]
				else:
					title = title + str(" ") + line.partition("      ")[2]


			#The first line after the title always begins with '<https://www.youtube.com/watch?v=' so we can use that to tell us where to stop looking for title.
			#Since done looking for title, we can also upload it.
			#The video URL will also be there, so we get that at the same time.
			#URL_Identifier is the video ID that is found with a URL search and will be set as part of the URL in Odysee.
			#Full_URL is the original URL that we will be linking to in the video description.


		if Looking_For_Title == 1 and str('      <https://www.youtube.com/watch?v=') in line:
			#Flag the variable to stop looking for title.
			Looking_For_Title = 0

			#Get the URL identifier from partitioning the line. We will need this for filepaths and to put in the new URL on Odysee.
			Video_ID = line.partition('watch?v=')[2]
			Video_ID = Video_ID.partition('&list=')[0]

			#Get the full URL of the original video so we can link it in the video description.
			Full_URL = line.partition('<')[2]
			Full_URL = Full_URL.partition("&list")[0]

			#Get rid of enter keys, in the case of videos whose titles spanned multiple lines. Do some printing while we're at it.
			title = title.replace("\n", "")
			print("Title is: " + title)
			print("URL Identifier is: " + Video_ID)
			print("Full URL is: " + Full_URL)



			#ACTUALLY IMPORTANT STUFF HERE: BASICALLY: GO TO THE URL, DETERMINISTICALLY DETERMINED FROM VIDEO ID FROM PLAYLIST AND SAVE IT 
			#AS A FILE NAME ALSO DETERMINED DETERMINISTICALLY FROM PLAYLIST AND WHERE WE TOLD IT TO SAVE AND ALSO ITS ALWAYS PNG.
			THINGY = (STUFF + "/" + convert_To_Filename(title) + " [" + Video_ID + "].png")


			link = "https://img.youtube.com/vi/" + Video_ID + "/hqdefault.jpg" #CHANGE THIS IF YOU NEED TO REDUCE RES
			print(link)

			if video_number >= video_start and video_number <= video_end:


				response = requests.get(link).content
				image_file = io.BytesIO(response)
				image  = Image.open(image_file)
				with open(link.split('/')[-1] , "wb") as f:
					image.save(THINGY)
					print("Success!!!!")



#			page.locator("xpath=/html/body/div[2]/div[1]/div/div/div[2]/input").fill(Full_URL)
#			page.locator("xpath=/html/body/div[2]/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/a[2]/img").saveAs(STUFF + video_filename + ".png")
