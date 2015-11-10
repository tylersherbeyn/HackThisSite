# String Manipulation HTS Mission 12
# https://www.hackthissite.org/missions/prog/12/
# Author: VectorStrain
# Date: 8/2/2015

#This level is about string manipulation.
#In this challenge, you will be given a string.
#Take all the numbers from the string and classify them as composite numbers or prime numbers.
#You should assume all numbers are one digit, and neither number 1 nor number 0 counts.
#Find the sum of every composite number, then find the sum of every prime number.
#Multiply these sums together.
#Then, take the first 25 non-numeric characters of the given string and increment their ASCII value by one (for example, # becomes $).
#Take these 25 characters and concatenate the product to them. This is your answer.
#Your answer should look like this: oc{lujxdpb%jvqrt{luruudtx140224

                                                    
import mechanize, os, cookielib, urllib, sys, re, lxml
from lxml import html
from bs4 import BeautifulSoup
from PIL import Image

number = ['2','3','4','5','6','7','8','9']
prime = ['2','3','5','7']
primesum = 0
composite = ['4','6','8','9']
compositesum = 0
string = ''
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
br.open("https://www.hackthissite.org/missions/prog/12/")
br.select_form(nr=0)
br.form['username'] = '********' #Enter User Name Here
br.form['password'] = '********' #Enter Password Here
br.submit()

#html = 
#soup = 
text = str(BeautifulSoup(br.response().read()))

text = re.sub('[\W\w\s]*<input type="text" value="','',text)
text = re.sub('"/><br/><br/>[\W\w\s]*','',text)


#print text
characters = list(text)
i = 0
characters.remove("1")
characters.remove("0")
for character in characters:

    

    if character in number:
        if character in prime:
            primesum = primesum + int(character)
        if character in composite:
            compositesum = compositesum + int(character)

    elif i < 25:
            print character
            string = string + chr(ord(character)+1)
            i+=1

result = compositesum * primesum

answer = string + str(result) 



#answer = ''
print answer
br.select_form(nr=0)
br.form['solution'] = str(answer)
br.submit()
