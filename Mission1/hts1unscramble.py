# Unscrambler for HTS Mission 1
# https://www.hackthissite.org/missions/prog/1/
# Author: VectorStrain
# Date: 8/10/2015

import re, sys, mechanize, cookielib, urllib
from bs4 import BeautifulSoup

dict = open("wordlist.txt", "r")
dictlist = dict.readlines()
dict.close

dictlist2 = []

for word in dictlist:
    word = re.sub('\n','',word)
    word = ''.join(sorted(word, key=str.lower))
    dictlist2.append(word)   

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

br.open("https://www.hackthissite.org/missions/prog/1/")
br.select_form(nr=0)
br.form['username'] = '********' #Enter User Name Here
br.form['password'] = '********' #Enter Password Here
br.submit()

html = br.response().read()
soup = BeautifulSoup(html)

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)
text = re.sub('\n',' ',text)

text = re.sub('[\W\w\s]*List of scrambled words:','',text)
text = re.sub('Answer:[\W\w\s]*','',text)

wordlist = text.split()
wordlist2 = []
answers = []

for word in wordlist:
    word = ''.join(sorted(word, key=unicode.lower))
    wordlist2.append(word)

for word in wordlist2:
    if word in dictlist2:
        answer = dictlist[dictlist2.index(word)]
        answer = re.sub('\n','',answer)
        answers.append(answer)

result = ''
flag = 0
for answer in answers:
    if flag == 1 :
        result = result + "," + answer
    else :
        result = result + answer
        flag = 1       

print str(result)

br.select_form(nr=0)
br.form['solution'] = str(result)
br.submit()
