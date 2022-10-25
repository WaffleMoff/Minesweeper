#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 14:53:26 2021

@author: shenlu
"""
"""
#Erik Ely
#9/15/21
#OMH
In this project, I had to do a lot of testing and tweaking. 
For example, adding the gutters complicated how I would take certain coordinates from the minemap and put them on the display map. 
But I found through trial and error plus some mental visualization, I was able to make things work.
Before I started writing out all of my functions, I planned ahead what I would need to make and what my gameloop would be.
Then after that, I used both the guide and plan to write my program.
In my initial versions, I didn't have much repetition since I was still figuring out how to make everything work.
However, I later revised it using quickcheck (which helps me look at everything around a coordinate) to make repetition work
Sources:
#https://www.w3schools.com/python/ref_string_split.asp I used this to understand split()
"""
import random, sys
global xsize, ysize, bombs, bombcount, display, minemap, tempx, tempy, flag, turn, spacerev, loop, zerolist, checkaround, quickcheck
#xsize = int(sys.argv[1])
#ysize = int(sys.argv[2])
#bombs = int(sys.argv[3])
zerolist = []
quickcheck = [(-1, 1),(0, 1),(1, 1),(1, 0),(-1, 0),(-1, -1),(0, -1),(1, -1)]
#This gets the dimensions for the map and checks to make sure they aren't too big and don't have too many or too few bombs
def getdimensions():
    global xsize, ysize, bombs, bombcount, display, minemap, tempx, tempy, flag, turn, spacerev
    try:
        xsize = int(input("Please enter the X size of the map: "))
        ysize = int(input("Please enter the Y size of the map: "))
        bombs = int(input("Please enter the number of bombs to place in the map: "))
    except ValueError:
        print("\nPlease enter only numbers, no other characters")
        getdimensions()
    if xsize*ysize <= bombs:
        print("\nSorry, that is too many bombs to fit in the map. Please try again!")
        getdimensions()
    if bombs == 0:
        print("\nSorry, you need bombs to play minesweeper. Please try again!")
        getdimensions()        
    if xsize*ysize >= 225:
        print("\nSorry, that is too large of a map! Please try smaller dimensions")
        getdimensions()
    display = [["□" for x in range(xsize)] for y in range(ysize)]
    minemap = [[0 for y in range(xsize + 2)] for y in range(ysize + 2)]
    
#setting initial values for variables plus getting the dimensions for the first time
getdimensions()
tempx = 0
tempy = 0
flag = False
turn = 0
loop = 0
spacerev = 0
#xsize = 30
#ysize = 10
#bombs = 50
bombcount = 0


#placing bombs on the map and making sure adjacent spaces display the proper number by adding to them each time a bomb is placed
def placebombs():
    global xsize, ysize, bombs, bombcount, display, minemap
    while bombcount < bombs:
        tempy = random.randint(1,ysize)
        tempx = random.randint(1,xsize)
        #print(tempx, ", ", tempy)
        if minemap[tempy][tempx] == "*":
            pass
        else:
            minemap[tempy][tempx] = "*"
            bombcount +=1
            quickcount = 0
            
            while quickcount < 8:
                a = quickcheck[quickcount]
                quickx = a[1]
                quicky = a[0]
                #print(tempx+quickx, ", ", tempy+quicky)
                #print(quickx)
                #print(quicky)
                if minemap[tempy+quicky][tempx+quickx] == "*":
                    pass
                else:
                    minemap[tempy+quicky][tempx+quickx] += 1
                    #print(tempx+quickx, ", ", tempy+quicky)
                quickcount += 1
           
#This updates the display map by taking the user's inputs and changing the display to reveal the coordinates from the minemap
#it also displays flags
def updatedisplay():
    global xsize, ysize, bombs, bombcount, updatedisplay, minemap, tempx, tempy, flag, turn
    
    if turn > 0:
        if flag == True:
            if display[tempx][tempy] == "⚑":
                display[tempx][tempy] = "□"
            else: 
                display[tempx][tempy] = "⚑"
            flag = False
        else:
            display[tempx][tempy] = str(minemap[tempx+1][tempy+1])
        for row in display:
            for col in row:
                print(col, end = " ")
            print("")        
    else:
        for row in display:
            for col in row:
                print(col, end = " ")
            print("")            

#This gets the user's moves, makes sure they are valid, and checks if the user won or lost. It uses flag and spacerev to make sure the win conditions aren't effected by the user entering the same coordinates multiple times.
#It also checks if the win conditions are met
#The first turn has a different process than the subsequent turns. If it's the first turn, instructions are displayed and safeturn() is called.
#I also found that try and except functions were especially necessary here to make sure the program didn't break when the user inputted random characters.
def getcord():
    global xsize, ysize, bombs, bombcount, display, minemap, tempx, tempy, flag, turn, loop, flag, spacerev     
    flag = False
    if turn == 0:
        print("Moves should be entered in the following format: Xcord Ycord")
        print("For example, the move 1 1 would reveal the top left corner")
        print("Make sure to leave spaces in between. You may add a space and an F to place a flag.")
    Cordset = input("Please enter your next move: ")
    #I wasn't sure how split() worked originally, so I used the source above to understand its syntax.
    #What I've done here is turned Cordset into a list using split, then I use the values later on and store them in tempx, tempy
    Cordset = Cordset.split()
    try:
        tempy = int(Cordset[0]) - 1
        tempx = int(Cordset[1]) - 1
    except ValueError:
        print("\nPlease enter your choice in the proper format: _ _ _")
        print("\nDo not use any punctuation, it should like like this: Xcord Ycord F(if you want)")
        getcord()  
    except IndexError:
        print("\nPlease enter your choice in the proper format: _ _ _")
        print("\nDo not use any punctuation, it should like like this: Xcord Ycord F(if you want)")
        getcord()  
    if len(Cordset) > 2:
        flag = True

    
    try:  
        if turn == 0:
            turn = 1
            
            safeturn()
            if flag == False:
                spacerev += 1
            
            if minemap[tempx+1][tempy+1] == 0 and flag == False:
                zerolist.append((tempx, tempy))
                spacerev -= 1
                clearzeros()
            if spacerev == xsize*ysize - bombs:
                loop = 1
                updatedisplay()
                print("\nYou win!\n")
                updatedisplay()
                playagain()
        elif turn >= 1:
            turn += 1
            if minemap[tempx+1][tempy+1] == "*":
                if flag == False:
                    loop = 1
                    print("\nYou lose!")
                    updatedisplay()
                    playagain()
            if flag == True:
                if display[tempx][tempy] == "□":
                    pass
                elif display[tempx][tempy] == "⚑":
                    pass
                else:
                    print("\nYou can't flag an already revealed space!")
                    flag == False
                    getcord()
                
            if flag == False: 
                if display[tempx][tempy] == "□":
                    spacerev += 1
                elif display[tempx][tempy] == "⚑":
                    spacerev += 1
            if minemap[tempx+1][tempy+1] == 0 and flag == False:
                zerolist.append((tempx, tempy)) 
                spacerev -= 1
                clearzeros()           
            if spacerev == xsize*ysize - bombs:
                loop = 1
                updatedisplay()
                print("\nYou win!\n")
                updatedisplay()
                playagain()

    except IndexError:
        print("\nPlease enter valid coordinates. Those weren't in the map!")
        if turn == 1:
            turn = 0
        getcord()

        
#This makes it so that if you do choose a mine on turn one, it gets turned into a normal space. Then it updates the space you chose as well as the spaces around it
def safeturn():
    global xsize, ysize, bombs, bombcount, updatedisplay, minemap, tempx, tempy, flag, turn 
    if flag == False and minemap[tempx+1][tempy+1] == "*":
        minemap[tempx+1][tempy+1] = 0
        bombs -= 1
        
        quickcount = 0
            
        while quickcount < 8:
            a = quickcheck[quickcount]
            quicky = a[1]
            quickx = a[0]
            #print(tempx+quickx, ", ", tempy+quicky)
            #print(quickx)
            #print(quicky)
            if minemap[tempx+1+quickx][tempy+1+quicky] == "*":
                minemap[tempx+1][tempy+1] += 1
            else:
                minemap[tempx+1+quickx][tempy+1+quicky] -= 1
                #print(tempx+quickx, ", ", tempy+quicky)
            quickcount += 1

#This was used mostly for testing to make sure that all the numbers were correct. I've commented it out in the final version.
def displayminemap():
    global xsize, ysize, bombs, bombcount, display, minemap, tempx, tempy, flag, turn, loop    
    for row in minemap:
        for col in row:
            print(col, end = " ")
        print("")
#This is basically the plan that I came up with in the beginning. I knew that each time through, the display would have to update and I'd have to get a new move.
#This also places the bombs at the beginning
def gameloop():
    global xsize, ysize, bombs, bombcount, display, minemap, tempx, tempy, flag, turn, loop
    placebombs()
    while loop < 1:
        updatedisplay()
        #displayminemap()
        getcord()
        #print("This is the number of spaces revealed: ", spacerev)
#This lets the user play again. If they choose to do so, it resets all variables and gets a new set of dimensions before starting over again.
def playagain():
    global xsize, ysize, bombs, bombcount, display, minemap, tempx, tempy, flag, turn, spacerev, loop
    ans = input("Would you like to play again? (Type y for yes, n for no): ")
    if ans.lower() == "y":
        tempx = 0
        tempy = 0
        flag = False
        turn = 0
        loop = 0
        spacerev = 0
        #xsize = 30
        #ysize = 10
        bombs = 0
        bombcount = 0
        getdimensions()
        gameloop()
    elif ans.lower() == "n":
        print("\nThanks for playing!")
        sys.exit()
    else:
        print("\nSorry, I didn't understand you. Please try again!")
        playagain()
"""
This is the zero function. If user hits a zero, put the coordinates into a zeros list
while there are are items in the zeros list, it repeats the following:
reveal zero and all surrounding spaces
add zeros revealed to zeros list
finally remove the zero just used from the list

quickcheck is a list that makes it so that this can use a loop to check around a coordinate instead of manually doing it.
"""
def clearzeros():
    global xsize, ysize, bombs, bombcount, display, minemap, tempx, tempy, flag, turn, spacerev, loop, quickcheck
    
    try:
        
        while len(zerolist) > 0:
            quickcount = 0
            zerox = zerolist[0][0]
            #print(zerox)
            zeroy = zerolist[0][1]
            #print(zeroy)
            while quickcount < 8:
                a = quickcheck[quickcount]
                quickx = a[1]
                quicky = a[0]
                #print(quickx)
                #print(quicky)
                if zeroy + quicky > ysize-1 or zeroy + quicky < 0:
                    pass
                elif zerox + quickx > xsize-1 or zerox + quickx < 0:
                    pass
                elif display[zerox+quickx][zeroy+quicky] == "□":
                    display[zerox+quickx][zeroy+quicky] = minemap[zerox+1+quickx][zeroy+1+quicky]
                    spacerev += 1
                    if display[zerox+quickx][zeroy+quicky] == 0:
                        qcord = (zerox+quickx, zeroy+quicky)
                        zerolist.append(qcord)
                quickcount += 1  
            
            zerolist.pop(0)
            
    except IndexError:
        pass
    #print(spacerev)
    
gameloop()


