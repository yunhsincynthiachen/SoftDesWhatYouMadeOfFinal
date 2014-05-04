# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 21:28:04 2014

@author: Yun-Hsin Cynthia Chen, Mika Ichiki-Welches, Neal Singer, Jenny Vaccaro
"""
import os
import sys
import time
import Image
import PIL
from urllib import FancyURLopener
import urllib2
import simplejson
import pygame
import random
from pygame.locals import *
import string
import sys
import socket

'''''''''''''''''''''''''''User Interface Portion'''''''''''''''''''''''''''
pygame.init()

#Define colors:
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (100, 100, 200)

w = 640  #width of the screens
h = 480 #height of the screens

def get_key():
    '''Sets the Pygame Environment and Keys'''
    running = 1 #Sets running to 1
    while running: #While running is 1, the following is true
        event = pygame.event.poll() #Gets a single event
        if event.type == pygame.QUIT: #When pygame is uninitialized, running is set to 0
            running = 0 
        elif event.type == KEYDOWN: #When keys are pressed down, returns key letter and number
            return (event.key, event.unicode) #unicode makes capital letters and symbols possible
        else: #Else: Continues the running
            pass 
        
def display_box_file(screen,message):
    '''Sets the Display of the Screen When Player Enters Keyword, Input File and Output File'''
    fontobject = pygame.font.Font(None,40) #sets the font
    pygame.draw.rect(screen,(255,255,255),(0,0,w,h),0) #sets the background as white and as large as width and height set before
    pygame.draw.rect(screen,(random.randint(0,255),0,random.randint(0,255)),(0,(h/2)-15,w,50),0) #creates a rectangular object under text
    if len(message) != 0:
        screen.blit(fontobject.render(message,1,(0,random.randint(0,255),random.randint(0,255))),((w/2)-310,(h/2)-55)) #rendering of the text
    pygame.display.flip() #flips the display -> continually updates the screen

def get_keyword():
    screen = pygame.display.set_mode((w,h)) #Creates the screen
    question = "Type A Keyword" #Inputs the question of the screen
    pygame.font.init() #initializes the font
    list_string_keyword = [] #makes a list of every character person types in
    display_box_file(screen,question + ":" + string.join(list_string_keyword,""))#uses the display function to create the screen
    running = 1 #sets running to 1
    while running: #while running is 1
        (inkey, unichr) = get_key() #initializes the get_key() function
        print (inkey,unichr) #prints each character that is pressed
        if inkey == K_BACKSPACE: #when backspace is pressed, the previous key is removed
            list_string_keyword = list_string_keyword[0:-1]
        elif inkey == 13: #initializes the enter key
            keyword_string = str("".join(list_string_keyword)) #while join all of the strings in the list to a string
            return keyword_string
        elif inkey <= 127: #initializes all of the other keys and appends it to the list of keys pressed
            list_string_keyword.append(unichr)
        display_box_file(screen,question + ": " + string.join(list_string_keyword,"")) #while keep updating the screen

def get_file_name():
    screen = pygame.display.set_mode((w,h))#Creates the screen
    question = "Type File Name to Recreate" #Inputs the command on the screen
    pygame.font.init() #initializes the font
    list_string_filename = [] #makes a list of every character person types in
    display_box_file(screen,question + ":" + string.join(list_string_filename,"")) #uses the display function to create the screen
    running = 1 #sets running to 1
    while running: #while running is 1
        (inkey, unichr) = get_key() #initializes the get_key() function
        print (inkey,unichr) #prints each character that is pressed
        if inkey == K_BACKSPACE: #when backspace is pressed, the previous key is removed
            list_string_filename = list_string_filename[0:-1]
        elif inkey == 13: #initializes the enter key
            filename_string = str("".join(list_string_filename)) #while join all of the strings in the list to a string
            return filename_string
        elif inkey <= 127: #initializes all of the other keys and appends it to the list of keys pressed
            list_string_filename.append(unichr)
        display_box_file(screen,question + ": " + string.join(list_string_filename,"")) #while keep updating the screen
    

def get_output():
    screen = pygame.display.set_mode((w,h))#Creates the screen
    question = "Type A Cool Output File Name" #Inputs the command on the screen
    pygame.font.init() #initializes the font
    list_string_output = [] #makes a list of every character person types in
    display_box_file(screen,question + ":" + string.join(list_string_output,"")) #uses the display function to create the screen
    running = 1 #sets running to 1
    while running: #while running is 1
        (inkey, unichr) = get_key() #initializes the get_key() function
        print (inkey,unichr) #prints each character that is pressed
        if inkey == K_BACKSPACE: #when backspace is pressed, the previous key is removed
            list_string_output = list_string_output[0:-1]
        elif inkey == 13: #initializes the enter key
            output_string = str("".join(list_string_output)) #while join all of the strings in the list to a string
            return output_string
        elif inkey <= 127: #initializes all of the other keys and appends it to the list of keys pressed
            list_string_output.append(unichr)
        display_box_file(screen,question + ": " + string.join(list_string_output,"")) #while keep updating the screen
        
'''''''''''''''''''''''''''Home Page'''''''''''''''''''''''''''

class MenuItem(pygame.font.Font): 
    #Options Menu - creates the start and exit options in the menu as objects
    def __init__(self, text, font=None, font_size=30,
                 font_color=WHITE, (pos_x, pos_y)=(0, 0)):
        '''Initializes the text, font size, font color, and positions of the MenuItems'''
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y

    def is_mouse_selection(self, (posx, posy)):
        '''Recognizes whether or not the mouse pointer hovers over a MenuItem'''
        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and \
            (posy >= self.pos_y and posy <= self.pos_y + self.height):
                return True
        return False

    def set_position(self, x, y):
        '''Positions of MenuItems'''
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def set_font_color(self, rgb_tuple):
        '''Font color function to be set and changed later (to red) for feedback'''
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)

class GameMenu():
  	#Sets up Home Menu background
    def __init__(self, screen, items, funcs, bg_color=BLUE, font=None, font_size=70,
                 font_color=WHITE):
      	'''Initializes the color and screen of the GameMenu, as well as its title's font size and color'''
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.bg_color = bg_color
        self.funcs = funcs #functions associated with the MenuItems
        self.items = [] #list of MenuItems
        
        #Set title
        self.title = pygame.font.Font(None,70)
        self.text = self.title.render('What You Made Of!',1,(180,180,255))
        self.textpos = self.text.get_rect()
        self.textpos.centerx = self.screen.get_rect().centerx
        
        #Set description
        self.description = pygame.font.Font(None,35)
        self.ctext = self.description.render('A fantastical program for finding your true roots.',2,(0,0,0))
        self.cpos = self.ctext.get_rect()
        self.cpos.centerx = self.screen.get_rect().centerx #centered in the x dimension
        self.cpos.centery = self.screen.get_rect().centery - 155 #170 pixels above the center y position
        
        #Set directions
        self.directions = pygame.font.Font(None,35)
        self.dtext = self.directions.render('Make sure image file is in same file as code.',2,(243,243,21))
        self.dpos = self.dtext.get_rect()
        self.dpos.centerx = self.screen.get_rect().centerx #centered in the x dimension
        self.dpos.centery = self.screen.get_rect().centery - 120 #140 pixels above the center y position
        
        #Placement of MenuItems in home screen
        for index, item in enumerate(items):
            menu_item = MenuItem(item, font, font_size, font_color)

            t_h = len(items) * menu_item.height #total height of text block
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            pos_y = (self.scr_height / 2) - (t_h / 2) + (index * menu_item.height)
            
			#Appends the MenuItems to the GameMenu's self.items list
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

        self.mouse_is_visible = True
        self.cur_item = None

    def set_mouse_visibility(self):
      	'''Recognizes if the mouse is visible on the screen'''
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def set_keyboard_selection(self, key):
        '''Sets up the text font settings;
           Creates a red italic feedback when up and down keys are pressed'''
        for item in self.items:
            #Sets a neutral white, unitalicized font
            item.set_italic(False)
            item.set_font_color(WHITE)

        if self.cur_item is None:
            self.cur_item = 0
        else:
            # Find the chosen MenuItem
            if key == pygame.K_UP and \
                    self.cur_item > 0:
                self.cur_item -= 1
            elif key == pygame.K_UP and \
                    self.cur_item == 0:
                self.cur_item = len(self.items) - 1
            elif key == pygame.K_DOWN and \
                    self.cur_item < len(self.items) - 1:
                self.cur_item += 1
            elif key == pygame.K_DOWN and \
                    self.cur_item == len(self.items) - 1:
                self.cur_item = 0

        #Red and italicized for feedback
        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_font_color(RED)

        # If Enter or Space is pressed, run the item's function
        if key == pygame.K_SPACE or key == pygame.K_RETURN:
            text = self.items[self.cur_item].text
            self.mainloop = self.funcs[text]()

    def set_mouse_selection(self, item, mpos):
        '''Red italic feedback when an option is hovered over with the mouse'''
        if item.is_mouse_selection(mpos):
          	#If the mouse is detected over a MenuItem, the text becomes red and italicized
            item.set_font_color(RED)
            item.set_italic(True)
        else:
          	#Otherwise, it will be it's neutral white, unitalicized font
            item.set_font_color(WHITE)
            item.set_italic(False)

    def run(self):
        '''Initiates the home screen!'''
        self.mainloop = True
        while self.mainloop:
            mpos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                  	#Closes the mainloop when the pictures are done downloading so that the program can resume
                    self.mainloop = False
                elif event.type == pygame.KEYDOWN:
                    #If mouse isn't hovered over the screen, you can use the keyboard to select MenuItems
                    self.mouse_is_visible = False
                    self.set_keyboard_selection(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #If the mouse clicks an item, run its function
                    for item in self.items:
                        if item.is_mouse_selection(mpos):
                            self.mainloop = self.funcs[item.text]()

            if pygame.mouse.get_rel() != (0, 0):
                self.mouse_is_visible = True
                self.cur_item = None

            self.set_mouse_visibility()

            # Redraws the background so that it doesn't overlay with the italics
            self.screen.fill(self.bg_color)
            self.screen.blit(self.dtext,self.dpos)
            self.screen.blit(self.text,self.textpos)
            self.screen.blit(self.ctext,self.cpos)

            for item in self.items:
                if self.mouse_is_visible:
                    self.set_mouse_selection(item, mpos)
                self.screen.blit(item.label, item.position)

            #Updates the full display Surface to the screen
            pygame.display.flip()


'''''''''''''''''''''''''''Retriving the Pictures'''''''''''''''''''''''''''         
# Define search term
def getpicsyo(searchTerm, count): # Replace spaces ' ' in search term for '%20' in order to comply with request
    searchTerm = searchTerm.replace(' ','%20')
    
    
    # Start FancyURLopener with defined version 
    class MyOpener(FancyURLopener): 
        version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
    myopener = MyOpener()
    startcount = count    
    endcount = startcount + 3    
    # Set count to 0
    while count < endcount:
        for i in range(0,3):
            # Notice that the start changes for each iteration in order to request a new set of images for each loop
            url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm+'&start='+str(i*4)+'&userip=MyIP')
            #print url
            request = urllib2.Request(url, None, {'Referer': 'testing'})
            response = urllib2.urlopen(request)
            
            # Get results using JSON
            results = simplejson.load(response)
            data = results['responseData']
            dataInfo = data['results']
            
            # Iterate for each result and get unescaped url
            for myUrl in dataInfo:
                count = count + 1
                print count, myUrl['unescapedUrl']
                try:
                    myopener.retrieve(myUrl['unescapedUrl'],str(count)+'.jpg')
                except:
                    print 'Bad Download'
        # Sleep for one second to prevent IP blocking from Google
            time.sleep(1)
    return count    

'''''''''''''''''''''''''''''Cropping Picture'''''''''''''''''''''''''''  
def imgCrop(image,count,original_picture):
    '''image = string of image name, count = integer of image'''
    original_pic = picGrid(original_picture) 
    try: #resizes the image if there is an image found
        im = PIL.Image.open(image) #image is opened
        (x, y) =  im.size    #size is found
        if y < x: #if the length is longer
            box = (x/2-y/2, 0, x/2+y/2, y) #resize with length dominant
        else: #if the height is longer
            box = (0, y/2-x/2, x, y/2+x/2) #resize with height dominant
        region = im.crop(box) #crop image after with box size
        im1 = region.resize((original_pic.length,original_pic.length)) #imaage is resized to be consistent with others
        im1.save('CROPPED' + image) #saves each image under a name
    except: #if there is  a broken jpg print:
        print "bad image"

''''''''''''''''''''''''''''Finding Average RGB'''''''''''''''''''''''''''''
class PixelCounter(object):
  ''' loop through each pixel and average rgb '''
  def __init__(self, imageName):
      self.pic = Image.open(imageName) #open imageName that is defined
      # load image data
      self.imgData = self.pic.load() #loads the image
      
  def averagePixels(self):
      r, g, b = 0, 0, 0 #sets first rgb as 0,0,0
      count = 0 #counts total rgb's recorded
      for x in xrange(self.pic.size[0]): #goes through the whole image length
          for y in xrange(self.pic.size[1]): #goes through the whole image height
              ther,theg,theb = self.imgData[x,y] #finds the image rgb in each position
              r += ther #adds every r value to 0
              g += theg #adds every g value to 0
              b += theb #adds every b value to 0
              count += 1 #also counts the time it iterates through
      # calculate averages
      return (r/count), (g/count), (b/count) #creates tuple of average

'''''''''''''''''''''Create Dictionary with RGB and File Name'''''''''''''''
def createDictionary(prefix):
    '''Makes a dictionary linking RGB tuple to cropped image file.'''
    catdict = {} #the dictionary that we are making with each average RGB and cropped file
    
    for n in range(1,97):    #for each picture, it's making the number into a string
        n = str(n)
        try: #if image is good
            pc = PixelCounter(prefix + n + '.jpg') #use pixelcounter class
            (r, g, b) = pc.averagePixels() #finds average pixels
            catdict[prefix + n +'.jpg'] = (r, g, b) #adds the cropped file name with average pixels
        except: #prints 'bad pic' when image turns out to not be a JPG
            #When an image is too large or not the right file type #prints 'bad pic' when image turns out to not be a JPG
            print 'bad pic'
    return catdict #returns the whole created dictionary that we made

''''''''''''''''''''''Quadrant Positions Which Splits Picture'''''''''''''''   
class picGrid(object):
    ''' Makes a list of quadrant positions in which the picture is split upon into'''
    #quadrant is the vocabulary we are using to describe the square section of an image to map to

    def __init__(self, original_picture):
        '''Loads the input image and initializes its dimensions'''
        self.pic = original_picture #initializes the original image
        self.im = Image.open(self.pic) #opens original image
        self.imgheight, self.imgwidth = self.im.size #finds the size of the image
        self.length = self.imgheight/60 #finds the length of each quadrant box, splitting height into 70
    
    def get_quadrants(self):
        '''Breaks the input image into quadrants and creates a list of their x,y coordinates'''
        quadrant_origin_list = [] #makes a list of quadrants
        print self.imgheight, self.imgwidth #print each size
        for i in range(0,self.imgheight-self.length,self.length): #for the range of the total height split by the determined length
            for j in range(0,self.imgwidth-self.length,self.length): #for the range of the total width split by the determined length
                quadrant_origin_list.append((i, j)) #create a list that has each quadrant position
        return quadrant_origin_list #return the list
        
'''''''''''''''''Dictionary With RGB and Quadrant Positions'''''''''''''''''        
def pictionary(original_picture):
    '''Makes a dictionary linking RGB tuples to the coordinates of the quadrants of the cropped picture'''
    original = picGrid(original_picture) #initializes picGrid
    picdict = {} #creates a dictionary with RGB and quadrant positions
    quadrant_origin_list = original.get_quadrants() #get each quadrant list
    
    for quadrant in quadrant_origin_list: #for each quadrant, find position, crop each position and box and save it
        x, y = quadrant
        section = original.im.crop((x, y, x+original.length, y+original.length))
        section.save('section.jpg')        
        pc = PixelCounter("section.jpg") #then we find each average rgb for each section
        picdict[(x,y)] = pc.averagePixels() #place all of the average rgb values into dictionaries corresponding to position
    return picdict

'''''''''''''''''''Finds the Smallest Distance Between RGB'''''''''''''''''''
def RGBdistance(RGB,RGB2):
    """Find the distance between two RGB values"""
    r, g, b = RGB #one RGB value
    r2, g2, b2 = RGB2 #another RGB value
    #Uses the distance formula to find the distance between RGB and RGB2:
    distance = ((r2-r)**2 + (g2-g)**2 + (b2-b)**2)**(.5)
    return distance

'''''''''''''''''Uses RGB Distance To Find and match Similar RGB'''''''''''
def RGBmatch(dpicture,dimages):
    """For each quadrant of the picture, search through 
    the dictionary of images to find the image with the 
    smallest distance in RGB values"""
    
    RGBmatches = {}
    for quadrant, y in dpicture.items(): 
        d_old = 255*(3**(.5)) #farthest RGB distance possible
        for image, y in dimages.items():
          	#Loops through the images and each time it finds an image 
            #with a smaller distance from the quadrant, it replaces it as key_closest_image
            d = RGBdistance(dpicture[quadrant],dimages[image])
            if d < d_old:
                d_old = d
                key_closest_image = image
        RGBmatches[quadrant] = key_closest_image #creates a dictionary with each quadrant and its closest image match
    return RGBmatches

'''''''''''''''''Creates and Saves Final Image'''''''''''''''''''''''''''
def compileImage(RGBmatches,original_picture,output):
    '''Creates and saves our final image yayy!'''
    new_original = picGrid(original_picture) #we are creating a new image, initializes class picGrid
    newImage = Image.new(new_original.im.mode, new_original.im.size) #new image with have the size of the image created from original_picture dimensions
    for quadrant, imageName in RGBmatches.items(): #for each quadrant and image name in RGBmatches dictionary
        x, y = quadrant #find the quadrant as x and y
        im = Image.open(imageName) #open each image 
        newImage.paste(im,(x,y,x+new_original.length,y+new_original.length)) #in the new image, paste the image that corresponds
        newImage.save(output) #save the newImage after each time it runs through the for loop
    
if __name__ == "__main__":
    # defined global variables
    global keyword, input_file, output
    
    def choose():
        global keyword, input_file, output # we're gonna use these global variables
        #changes to next screen
        keyword = get_keyword() #uses get_keyword screen to get keyword
        input_file = get_file_name() #uses get_file_name screen to retrieve file name
        output = get_output() #uses get_output to get a name for output song
    
    # Creating the screen
    screen = pygame.display.set_mode((640, 480), 0, 32)

    menu_items = ('Recreate Yo Self','Exit')
    funcs = {'Recreate Yo Self': choose,'Exit':sys.exit}

    pygame.display.set_caption('Options Menu')
    gm = GameMenu(screen, funcs.keys(), funcs)
    gm.run()
    
    #part that runs through and creates new image
    colors = ["","red ", "blue ", "green ", "yellow ", "brown ", "black ", "tan "] #all the colors we want to run through
    c = 0 
    for i in colors: #get pics of the keyword with each color
        c = getpicsyo(i + keyword, c)
    for count in range(1,97):
        imgCrop(str(count) + '.jpg', count, input_file) #crops the image
    dpicture =  pictionary(input_file) #finds the dictionary of rgb and each section of the original image
    print createDictionary('CROPPED')
    dimages = createDictionary('CROPPED') #finds the dictionary of rgb and each keyword image
    #print dimages
    RGBmatches = RGBmatch(dpicture, dimages) #creates dictionary of each RGB match files and section location\
    print RGBmatches
    compileImage(RGBmatches, input_file, output) #creates and saves the final image
    Image.open(output) #opens the final image