# Unscrambler for HTS Mission 7
# https://www.hackthissite.org/missions/prog/7/
# Author: Tyler Sherbeyn
# Date: 5/3/2018

import re
import unscramble
from robobrowser import RoboBrowser
from PIL import Image
from random import randrange

def mostadjacent(list1, lists):
	count = 0
	black = (0,0,0)
	mostadjacent = []
	for list in lists:
		tempcount = 0
		for i in range(len(list1)-1):
			if list[i] != black:
				#print (list[i])
				if list[i] == list1[i]:
					tempcount+=1
				if( i < len(list1)-1):
					if list[i] == list1[i+1]:
						tempcount+=1
				if( i < 0):
					if list[i] == list1[i-1]:
						tempcount+=1
		if tempcount >= count:
			count = tempcount
			mostadjacent = list	
	return mostadjacent
	
def compare_lists(list1, list2):
	for element in list1:
		if element in list2:
			return True
	return False

def countcommonvalues(list1, list2):
	x = 0
	for element in list1:
		if element in list2:
			x+=1
	return x
	
def mostcommon(list1, lists):
	count = 0
	mostcommon = []
	for list in lists:
		if (countcommonvalues(list1, list) > count):
			count = countcommonvalues(list1, list)
			mostcommon = list
	return mostcommon
	
def find_closest(num, list1):
	diff = 10000
	tempelement = 0
	for element in list1:
		if(element - num < diff):
			diff = element - num
			tempelement = element
	return tempelement
	
def main():
	# Login
	url = 'https://www.hackthissite.org/missions/prog/7/'
	br = RoboBrowser(history=True, parser='html.parser')
	br.session.headers['Referer'] = url
	br.open(url)
	forms = br.get_forms()
	form = br.get_form(action="/user/login")
	form['username'].value = '*****'
	form['password'].value = '*****'
	form.serialize() 
	br.submit_form(form)

	# Get Image
	request = br.session.get(url+"BMP", stream=True)
	with open("BMP.PNG", "wb") as file:
		file.write(request.content)
	im = Image.open("BMP.PNG")
	pix = im.load()
	#im.show()
	
	# Convert Image Pixels to List
	lines = []
	for y in range(im.size[1]):
		pixels = []
		for x in range(im.size[0]):
			pixels.append(pix[x,y])
		lines.append(pixels)
		
	# Dominate Background Colors
	c = 0
	first = 0
	firstcount = 0
	second = 0
	secondcount = 0
	while c < 255:
		i = 0
		for line in lines:
			for pixel in lines:
				if pixel[0][0] == c:
					i+=1
		if i > secondcount and i < firstcount:
			second = c
			secondcount = i
		if i > firstcount:
			second = first
			secondcount = firstcount
			first = c
			firstcount = i
		c+=1
		
	# # Gets Values of Lines
	# colors = []
	# values = []
	# for line in lines:
		# v = 0
		# for pixel in lines:
			# temppixel = []
			# for value in pixel:
				# for val in value:
					# v = v + val
		# values.append(v)
		
	# # Sorts By Value
	# sorted_values = sorted(range(len(values)),key=lambda x:values[x])
	# sorted_lines = [lines[i] for i in sorted_values ]
	# lines = sorted_lines
	
	# Create Temp Lines Array
	# templines = lines
	# sortedlines = []
	# #Adds Initial Line To Array
	# index = randrange(0,len(lines))
	# #index = values.index(max(values))
	# line = templines[index]
	# sortedlines.append(line)
	# templines.remove(line)
	# #Sorts Lines by Closests Lines
	# thelines = lines
	# for i in range(len(thelines)):
		# templine = mostcommon(sortedlines[i], templines)
		# templines.remove(templine)
		# sortedlines.append(templine)
	# lines = sortedlines
	
	#Removes Background
	templines = []
	for line in lines:
		templine = []
		for pixel in line:
			temppixel = []
			if pixel[0] == first or pixel[0] == second:
				templine.append((0,0,0))
			else:
				templine.append(pixel)
		templines.append(templine)
	lines = templines
	templines = []
	for line in lines:
		templine = []
		tempcolor = ()
		for pixel in line:
			temppixel = []
			if pixel != (0,0,0) and tempcolor == ():
				tempcolor = pixel
			if pixel != tempcolor:
				templine.append((0,0,0))
			else:
				templine.append(pixel)
		templines.append(templine)
	lines = templines
	
	# Create Temp Lines Array
	templines = lines
	sortedlines = []
	
	# Adds Initial Line To Array
	index = randrange(0,len(lines))
	line = templines[index]
	sortedlines.append(line)
	templines.remove(line)
	
	#Sorts Lines by Most Adjacent Lines
	for i in range(len(lines)):
		templine = mostadjacent(sortedlines[i], templines)
		templines.remove(templine)
		sortedlines.append(templine)
	lines = sortedlines
	
	# Convert List of Manipulated Pixels back to Image and show
	im2 = Image.new(im.mode, [200, len(sortedlines)])
	temppixels = im2.load()
	for y in range(im2.size[1]):
		for x in range(im2.size[0]):
			temppixels[x,y] = lines[y][x]
	#print(im2.size)
	im2.show()

	form = br.get_form()
	form['solution'].value = input("Solution: ")
	form.serialize() 
	br.submit_form(form)
	print(re.sub('<.*?>', ' ', str(br.select("center"))))

if __name__ == '__main__':
  main()