# Image Analyzer for HTS Mission 2
# https://www.hackthissite.org/missions/prog/2/PNG/
# Author: Tyler Sherbeyn
# Date: 2/25/2015

import mechanize, os, cookielib, urllib, sys, re
from bs4 import BeautifulSoup
from PIL import Image

CODE = { '.-': 'A',    '-...': 'B',   '-.-.': 'C', 
        '-..': 'D',    '.': 'E',      '..-.': 'F',
        '--.': 'G',    '....': 'H',   '..': 'I',
        '.---': 'J',   '-.-': 'K',    '.-..': '',
        '--': 'M',     '-.': 'N',     '---': 'O',
        '.--.': 'P',   '--.-': 'Q',   '.-.': 'R',
     	'...': 'S',    '-': 'T',      '..-': 'U',
        '...-': 'V',   '.--': 'W',    '-..-': 'X',
        '-.--': 'Y',   '--..': 'Z',
        
        '-----': '0',  '.----': '1',  '..---': '2',
        '...--': '3',  '....-': '6',  '.....': '5',
        '-....': '6',  '--...': '7',  '---..': '8',
        '----.': '9' 
        }

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
br.open("https://www.hackthissite.org/missions/prog/2/")
br.select_form(nr=0)
br.form['username'] = '********' # Enter Username
br.form['password'] = '********' # Enter Password
br.submit()

#   Retrieve Image
br.retrieve('https://www.hackthissite.org/missions/prog/2/PNG', 'PNG.png')

# Open Image
im = Image.open('PNG.png' , 'r' )

pix_val = list(im.getdata())

list = []
#print pix_val
i=0
oldpos = 0
newpos = 0
diff = 0

for pixel in pix_val:
    if pixel == 1:
        oldpos = newpos
        newpos = i
        diff = newpos - oldpos
        list.append(diff)
    i += 1
    
result = ''
for char in list:
    if char == 47:
        result = result + " / "
    if char == 46:
        result = result + "."
    if char == 45:
        result = result + "-"
    if char == 32:
        result = result + " "
        

print result
codes = result.split()
result = ''
slash = '/'
for code in codes:
    if code == slash:
        result = result + '/'
    else:
        result = result + CODE[code]

#print codes
print result
br.select_form(nr=0)
br.form['solution'] = str(result)
br.submit()
