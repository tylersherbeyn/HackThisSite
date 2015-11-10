# XML Parsing for HTS Mission 4
# https://www.hackthissite.org/missions/prog/4/XML
# Author: VectorStrain
# Date: 10/17/2015

import mechanize, os, cookielib, urllib, sys, re, bz2, Image, ImageDraw
from bs4 import BeautifulSoup
import pygame
from pygame import transform
from math import pi

def degreesToRadians(deg):
    return (deg)/180.0 * pi

# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
YELLOW =(255, 255,   0)
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)

# Set the height and width of the screen
screen = pygame.display.set_mode([800, 800])

pygame.display.set_caption("Draw Some Strings")

#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

br = mechanize.Browser()
cj = cookielib.CookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)

#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# User-Agent
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.open("https://www.hackthissite.org/missions/prog/4/")
br.select_form(nr=0)
br.form['username'] = '********'
br.form['password'] = '********'
br.submit()

# Gets the File 
br.retrieve('https://www.hackthissite.org/missions/prog/4/XML', 'plotMe.xml.bz2')

# Reads File
bz_file = bz2.BZ2File("plotMe.xml.bz2")
line_list = bz_file.readlines()

current_color = ''

line_blue_x_start = []
line_blue_x_end = []
line_blue_y_start = []
line_blue_y_end = []

arc_blue_x_center = []
arc_blue_extend = []
arc_blue_y_center = []
arc_blue_start = []
arc_blue_radius = []

line_green_x_start = []
line_green_x_end = []
line_green_y_start = []
line_green_y_end = []

arc_green_x_center = []
arc_green_extend = []
arc_green_y_center = []
arc_green_start = []
arc_green_radius = []

line_red_x_start = []
line_red_x_end = []
line_red_y_start = []
line_red_y_end = []

arc_red_x_center = []
arc_red_extend = []
arc_red_y_center = []
arc_red_start = []
arc_red_radius = []

line_yellow_x_start = []
line_yellow_x_end = []
line_yellow_y_start = []
line_yellow_y_end = []


arc_yellow_x_center = []
arc_yellow_extend = []
arc_yellow_y_center = []
arc_yellow_start = []
arc_yellow_radius = []

line_white_x_start = []
line_white_x_end = []
line_white_y_start = []
line_white_y_end = []

arc_white_x_center = []
arc_white_extend = []
arc_white_y_center = []
arc_white_start = []
arc_white_radius = []

rx = re.compile(r'[^\d.-]+')

current_color = ''

line_start_flag = False
line_end_flag = False

arc_start_flag = False
arc_end_flag = False

# Line Attributes
x_start = ''
y_start = ''
x_end = ''
y_end = ''

# Arc Attributes
x_center = ''
extend = ''
y_center = ''
start = ''
radius = ''

for line in line_list:
    line = re.sub('\n','',line )
    #print line

    if "<Line>" in line:
        line_start_flag = True
        line_end_flag = False
        arc_start_flag = False
        arc_end_flag = False
        current_color = 'white'

    if "</Line>" in line:
        line_end_flag = True
        line_start_flag = False
        arc_start_flag = False
        arc_end_flag = False

    if "<Arc>" in line:
        arc_start_flag = True
        arc_end_flag = False
        line_end_flag = False
        line_start_flag = False
        current_color = 'white'

    if "</Arc>" in line:
        arc_end_flag = True
        arc_start_flag = False
        line_end_flag = False
        line_start_flag = False

    if "<Color>" in line and line_start_flag == True or arc_start_flag == True:
        if 'red' in line:
            current_color = 'red'
        if 'blue' in line:
            current_color = 'blue'
        if 'yellow' in line:
            current_color = 'yellow'
        if 'green' in line:
            current_color = 'green'
        if 'white' in line:
            current_color = 'white'
            
    if "<XStart>" in line and line_start_flag == True:
        x_start = (float)(rx.sub('',line))
    if "<YStart>" in line and line_start_flag == True:
        y_start = -1*(float)(rx.sub('',line))+800
    if "<XEnd>" in line and line_start_flag == True:
        x_end = (float)(rx.sub('',line))
    if "<YEnd>" in line and line_start_flag == True:
        y_end = -1*(float)(rx.sub('',line))+800
    if "<XCenter>" in line and arc_start_flag == True:
        x_center = (float)(rx.sub('',line))
    if "<YCenter>" in line and arc_start_flag == True:
        y_center = -1*(float)(rx.sub('',line))+800
    if "<ArcStart>" in line and arc_start_flag == True:
        start = (float)(rx.sub('',line))
        print line
        print start
    if "<ArcExtend>" in line and arc_start_flag == True:
        extend = (float)(rx.sub('',line))
        print line
    if "<Radius>" in line and arc_start_flag == True:
        radius = (float)(rx.sub('',line))

    # Set Line Properties
    if line_start_flag == False and line_end_flag == True and arc_start_flag == False and arc_end_flag == False:
        line_end_flag = False
        if current_color == 'blue':
            line_blue_x_start.append(x_start)
            line_blue_y_start.append(y_start)
            line_blue_x_end.append(x_end)
            line_blue_y_end.append(y_end)
        if current_color == 'green':
            line_green_x_start.append(x_start)
            line_green_y_start.append(y_start)
            line_green_x_end.append(x_end)
            line_green_y_end.append(y_end)
        if current_color == 'red':
            line_red_x_start.append(x_start)
            line_red_y_start.append(y_start)
            line_red_x_end.append(x_end)
            line_red_y_end.append(y_end)
        if current_color == 'yellow':
            line_yellow_x_start.append(x_start)
            line_yellow_y_start.append(y_start)
            line_yellow_x_end.append(x_end)
            line_yellow_y_end.append(y_end)
        if current_color == 'white':
            line_white_x_start.append(x_start)
            line_white_y_start.append(y_start)
            line_white_x_end.append(x_end)
            line_white_y_end.append(y_end)

    # Set Arc Properties
    if arc_start_flag == False and arc_end_flag == True and line_start_flag == False and line_end_flag == False:
        arc_end_flag = False
        if current_color == 'blue':
            arc_blue_x_center.append(x_center)
            arc_blue_y_center.append(y_center)
            arc_blue_extend.append(start)
            arc_blue_start.append(extend)
            arc_blue_radius.append(radius)
        if current_color == 'green':
            arc_green_x_center.append(x_center)
            arc_green_y_center.append(y_center)
            arc_green_extend.append(start)
            arc_green_start.append(extend)
            arc_green_radius.append(radius)
        if current_color == 'red':
            arc_red_x_center.append(x_center)
            arc_red_y_center.append(y_center)
            arc_red_extend.append(start)
            arc_red_start.append(extend)
            arc_red_radius.append(radius)
        if current_color == 'yellow':
            arc_yellow_x_center.append(x_center)
            arc_yellow_y_center.append(y_center)
            arc_yellow_extend.append(start)
            arc_yellow_start.append(extend)
            arc_yellow_radius.append(radius)
        if current_color == 'white':
            arc_white_x_center.append(x_center)
            arc_white_y_center.append(y_center)
            arc_white_extend.append(start)
            arc_white_start.append(extend)
            arc_white_radius.append(radius)

# Debugging coordinates
'''i = 0
for coord in line_white_x_start:
   print line_white_x_start[i]
    print line_white_y_start[i]
    print line_white_x_end[i]
    print line_white_y_end[i]
    i+=1
'''

i = 0
for coord in arc_blue_x_center:
    print "x_center " + str(arc_blue_x_center[i])
    print "y_center " + str(arc_blue_y_center[i])
    print "radius " + str(arc_blue_radius[i])
    print "extend " + str(arc_blue_extend[i])
    print "start " + str(arc_blue_start[i])
    i+=1


# Loop for Pygame display
while not done:
    
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(10)
    
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
            
    # All drawing code happens after the for loop and but
    # inside the main while done==False loop.

    # Clear the screen and set the screen background
    screen.fill(BLACK)
    
    #Draw Lines # TO DO: Compare i to len of list and if less draw else pass
    i = 0
    for coord in line_blue_x_start:
        pygame.draw.line(screen, BLUE, [line_blue_x_end[i], line_blue_y_end[i]],[line_blue_x_start[i], line_blue_y_start[i]], 1) 
        i+=1
    i = 0
    for coord in arc_blue_start:
        rect = (arc_blue_x_center[i]-arc_blue_radius[i],arc_blue_y_center[i]-arc_blue_radius[i],arc_blue_radius[i]*2,arc_blue_radius[i]*2)
        pygame.draw.arc(screen, BLUE, rect, degreesToRadians((arc_blue_extend[i])) , degreesToRadians(arc_blue_extend[i]+arc_blue_start[i]), 1 )
        i+=1
    i = 0
    for coord in line_green_x_start:
        pygame.draw.line(screen, GREEN, [line_green_x_start[i], line_green_y_start[i]],[line_green_x_end[i], line_green_y_end[i]], 1) 
        i+=1
    i = 0
    for coord in arc_green_start:
        rect = (arc_green_x_center[i]-arc_green_radius[i],arc_green_y_center[i]-arc_green_radius[i],arc_green_radius[i]*2,arc_green_radius[i]*2)
        pygame.draw.arc(screen, GREEN, rect, degreesToRadians((arc_green_extend[i])) , degreesToRadians(arc_green_extend[i]+arc_green_start[i]), 1 )
        i+=1
    i = 0
    for coord in line_red_x_start:
        pygame.draw.line(screen, RED, [line_red_x_start[i], line_red_y_start[i]],[line_red_x_end[i], line_red_y_end[i]], 1) 
        i+=1
    i = 0
    for coord in arc_red_start:
        rect = (arc_red_x_center[i]-arc_red_radius[i],arc_red_y_center[i]-arc_red_radius[i],arc_red_radius[i]*2,arc_red_radius[i]*2)
        pygame.draw.arc(screen, RED, rect, degreesToRadians((arc_red_extend[i])) , degreesToRadians(arc_red_extend[i]+arc_red_start[i]), 1 )
        i+=1
    i = 0
    for coord in line_yellow_x_start:
        pygame.draw.line(screen, YELLOW, [line_yellow_x_start[i], line_yellow_y_start[i]],[line_yellow_x_end[i], line_yellow_y_end[i]], 1)
        i+=1
    i = 0
    for coord in arc_yellow_start:
        rect = (arc_yellow_x_center[i]-arc_yellow_radius[i],arc_yellow_y_center[i]-arc_yellow_radius[i],arc_yellow_radius[i]*2,arc_yellow_radius[i]*2)
        pygame.draw.arc(screen, YELLOW, rect, degreesToRadians((arc_yellow_extend[i])) , degreesToRadians(arc_yellow_extend[i]+arc_yellow_start[i]), 1 )
        i+=1
    i = 0
    for coord in line_white_x_start:
        pygame.draw.line(screen, WHITE, [line_white_x_start[i], line_white_y_start[i]],[line_white_x_end[i], line_white_y_end[i]], 1) 
        i+=1
    i = 0
    for coord in arc_white_start:
        rect = (arc_white_x_center[i]-arc_white_radius[i],arc_white_y_center[i]-arc_white_radius[i],arc_white_radius[i]*2,arc_white_radius[i]*2)
        pygame.draw.arc(screen, WHITE, rect, degreesToRadians((arc_white_extend[i])) , degreesToRadians(arc_white_extend[i]+arc_white_start[i]), 1 )
        i+=1
    i = 0
    
    pygame.display.flip()
    
# Be IDLE friendly
pygame.quit()

#BlueStringHere,GreenStringHere,RedStringHere,YellowStringHere,WhiteStringHere
br.select_form(nr=0)
br.form['solution'] = raw_input("BlueGreenRedYellowWhite: ")
br.submit()
