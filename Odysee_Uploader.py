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
from playwright.sync_api import sync_playwright

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
	video_filename = video_filename.replace('"', '＂')

	video_filename = video_filename.replace("|", "｜") # I don't have a clue why it would do this since they're both
	video_filename = video_filename.replace(":", "：")# allowed characters, but ah well.
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



print("What is your Odysee email?")# GET LOGIN INFO FROM USER
LOGIN_EMAIL = input()
while LOGIN_EMAIL == "BLANK":
	time.sleep(0.5)

print("What is your Odysee password? (I promise this will not be recorded outside of using this program)")
LOGIN_PW = getpass()
while LOGIN_PW == "BLANK":
	time.sleep(0.5)

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

print("What is the folder that your video, thumbnail,and description files located?")
STUFF = input()
while STUFF == "BLANK":
	time.sleep(0.5)

#Obligatory Playwright boiler plate code. The rest of the program will be performed under here.
with sync_playwright() as p:
	#Open browser
	browser = p.chromium.launch(headless = False)
	page = browser.new_page()
	page.goto("https://odysee.com/$/signin")

	#Enter the username and click it.
	page.locator("xpath=/html/body/div[1]/div/div[4]/div/main/section/div/div/section/div[1]/div[2]/div/form/fieldset-section/input").fill(LOGIN_EMAIL)
	page.locator("xpath=/html/body/div[1]/div/div[4]/div/main/section/div/div/section/div[1]/div[2]/div/form/div/button[1]/span/span").click()

	#Enter the password and click it.
	page.locator("xpath=/html/body/div[1]/div/div[4]/div/main/section/div/div/section/div/div[2]/form/fieldset-section/input").fill(LOGIN_PW)
	page.locator("xpath=/html/body/div[1]/div/div[4]/div/main/section/div/div/section/div/div[2]/form/div[2]/button[1]/span/span").click()


	#Wait for confirmation email to be accepted.
	time.sleep(5)
	while page.query_selector("xpath=/html/body/div[1]/div/div[4]/div/main/section/div/div/div/section/div/div[2]/div/button[1]/span/span") is not None:
		time.sleep(2)

	songs = codecs.open(str(song_file))


#now = datetime.now()
#today = date.today()

#Current_Time = today.strftime("%d_%m_%Y")+"_With_Time:"+now.strftime("%H:%M:%S")
#LOG_FILE = open("Uploadathon_Log_On_Date:"+str(Current_Time)+".txt", "x") # MAKE THE LOG FILE. THIS IS FUCKING IMPORTANT.


	for line in songs:  # GET THE FILE CONTAINING ALL OUR SONG TITLES + URLS AND SET TO VARIABLES SO WE CAN TYPE THEM IN
		line_num += 1 # Keep track of what line we're on.
		if str("Now playing") in line:
			video_number += 1 # Keep track of what video we're on by using a string that appears once per video.
			if video_number >= video_start and video_number <= video_end: # We want to increase the video number always so we know where we are, but only actually upload if the video number is within specifications.
				print("\n\nnow on video number " + str(video_number) + ":")
				title = "" #VERY IMPORTANT OR IT WILL GET INFINITELY LONG
			

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
		if Looking_For_Title == 1 and str('      <https://www.youtube.com/watch?v=') in line and video_number >= video_start and video_number <= video_end:
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

			#We can expect the uploader's channel URL to be two lines later, so we get ready for it.
			Look_For_Channel_URL = line_num + 2

			#I have no idea what this does. Might delete.
			Start_Upload = line_num + 6

			#Click the video uploader and select the video file.



		# If the current line number equals the Look_For_Channel_URL variable, which we set two lines prior, we know we're two lines later.
		# Use the line to get the uploader's channel's URL.
		if Look_For_Channel_URL == line_num:		
			Channel_URL_Part_One = line.partition("https://www.youtube.com/")[2]
			Channel_URL_Part_Two = Channel_URL_Part_One.partition('>')[0]
			Channel_URL = str('https://www.youtube.com/') + str(Channel_URL_Part_Two)
			Look_For_Channel_Name = line_num + 2


		# This is technically gratuitous since the channel name is also on the same line as we got the URL from.
		# I don't feel like changing it RN, due to accuracy concerns, and because I'm lazy (REMEMBER TO EDIT THAT OUT IF YOU USE THIS TO APPLY FOR A JOB).
		# In addition to containing the channel name, the line with the channel name is important because it means we've obtained all information 
		# necessary to upload the video. The remaining logic can be done in this under this if.
		if Look_For_Channel_Name == line_num:
			#Get channel name
			Channel_Name = str(line)

			#Go to upload page.
			page.goto("https://odysee.com/$/upload")

			#Click video upload button and select the applicable file.
			with page.expect_file_chooser() as fc_info:
				page.locator("xpath=/html/body/div[1]/div/div[4]/div[2]/main/div/section[1]/div/div/div/section/div/div/fieldset-section/input-submit/button/span/span").click()
			file_chooser = fc_info.value
#			filepath = STUFF + "/" + convert_To_Filename(title) + " [" + Video_ID
#			print(convert_To_Filename(title) + "THIS IS CONVERTED!!!!!!")
			file_chooser.set_files(STUFF + "/" + convert_To_Filename(title) + " [" + Video_ID + "].mp4")

			#Fill title field.
			page.locator("xpath=/html/body/div[1]/div/div[4]/div[2]/main/div/section[1]/div/div/div/section/div/div/div[1]/fieldset-section/input").clear()
			page.locator("xpath=/html/body/div[1]/div/div[4]/div[2]/main/div/section[1]/div/div/div/section/div/div/div[1]/fieldset-section/input").fill(title)

			#Fill the url field.
			page.locator("xpath=/html/body/div[1]/div/div[4]/div[2]/main/div/section[1]/div/div/div/section/div/div/fieldset-group/fieldset-section[2]/input").clear()
			page.locator("xpath=/html/body/div[1]/div/div[4]/div[2]/main/div/section[1]/div/div/div/section/div/div/fieldset-group/fieldset-section[2]/input").fill(Video_ID)

			#Fill the description field, with original url, uploader name, and uploader url from previously acquired variables, and the original
			#description, by reading the .description file.
			Description_File = codecs.open(STUFF+"/"+convert_To_Filename(title)+" ["+str(Video_ID)+"].description", "r")
			page.locator("xpath=/html/body/div[1]/div/div[4]/div[2]/main/div/section[2]/div/div[2]/div/section/div/div/fieldset-section/div/div/div/textarea[1]").fill("This was uploaded by an AI. Original URL was/is: " + Full_URL + "\nOriginal uploader name was/is: " + Channel_Name + "Original uploader's channel's URL was/is: " + Channel_URL + "\nOriginal, title, and thumbnail have been typed and uploaded here. Original description was/is:\n" + Description_File.read())

			#UPLOAD THUMBNAIL
			with page.expect_file_chooser() as fc_info:
				page.locator("xpath=/html/body/div[1]/div/div[4]/div[2]/main/div/div/section[1]/div/div[2]/div/div/div[2]/fieldset-section/input-submit/button/span/span").click()
			file_chooser = fc_info.value
			file_chooser.set_files(STUFF + "/" + title.replace('/', '⧸') + " [" + Video_ID + "].png") #VERY IMPORANT ON THIS ONE: AS OF RIGHT NOW I AM USING AN ALTERNATIVE METHOD OF THUMBNAIL DOWNLOAD WHICH DOES NOT APPLY THE SAME ARTIFACTS. KEEP THIS IN MIND!!!~

			#Confirm thumbnail upload.
			page.locator("xpath=/html/body/div[5]/div/div/div[2]/button[1]/span/span").click()

			#Add a tag (this may need to be customizable for the end user, but for now fuck it)
			page.locator("xpath=/html/body/div[1]/div/div[4]/div[2]/main/div/div/section[3]/div/div/div/section/div/div/form/fieldset-section[1]/fieldset-section/input").fill("music\n")
			page.locator("xpath=/html/body/div[1]/div/div[4]/div[2]/main/div/div/section[3]/div/div/div/section/div/div/form/fieldset-section[1]/fieldset-section/input").press('Enter')

			#Click the upload button.
			page.locator("xpath=/html/body/div[1]/div/div[4]/div[2]/main/div/section[3]/div/button/span/span").click()

			#Click the confirm button.
			page.locator("xpath=/html/body/div[5]/div/div/form/section/div/div[3]/div[1]/button[1]/span/span").click()

			#Do not continue until it confirms the upload is successful.
			while True:
				if page.query_selector("xpath=/html/body/div[5]/div/div/section/div/div[3]/div/button[1]/span/span") is None:
					time.sleep(2)
				else:
					break
			title = ""


			if video_number == video_end:
				print("Uploads complete. The program will now stall for an hour to give you time to perform any additional actions.")
				time.sleep(3600)





				#Loop_Toggle = 1
				#print("okay we're at the end of the loop")
				#LOG_FILE.write('Video "'+str(title)+'" successfully uploaded! \n \n \n')


