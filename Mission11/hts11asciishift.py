# ASCII SHIFT HTS Mission 11
# https://www.hackthissite.org/missions/prog/11/
# Author: Tyler Sherbeyn
# Date: 8/14/2015

#This string was randomly generated.
#It will not be recognizable text.
#You have 3 seconds to take the information from the website, and apply that to your algorithm. 

import mechanize, os, cookielib, urllib, sys, re, lxml
from lxml import html
from bs4 import BeautifulSoup
from PIL import Image

answer = ''

br = mechanize.Browser()
cj = cookielib.CookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)

#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.open("https://www.hackthissite.org/missions/prog/11/")
br.select_form(nr=0)
br.form['username'] = '********' #Enter User Name Here
br.form['password'] = '********' #Enter Password Here
br.submit()

text = BeautifulSoup(br.response().read()).get_text()   

string = text[text.find("Generated String: ")+18:text.find("Shift:")]
string = re.sub('\W',' ',string)
characters = string.split()

shift=text[text.find("Shift:")+7:text.find("Decoded ASCII")]

for character in characters:
    answer = answer + chr(int(character)-int(shift))

#print answer
br.select_form(nr=0)
br.form['solution'] = str(answer)
br.submit()
