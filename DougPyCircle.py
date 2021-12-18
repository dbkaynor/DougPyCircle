# flake8 --extend-ignore=E501 "%f"
# https://sites.cs.ucsb.edu/~pconrad/cs5nm/topics/pygame/drawing/
# http://cs.roanoke.edu/Fall2013/CPSC120A/pygame-1.9.1-docs-html/ref/examples.html
# https://www.geeksforgeeks.org/creating-start-menu-in-pygame/

import math
import os
import platform
import random
import sys
import tkinter
from tkinter.colorchooser import askcolor
from screeninfo import get_monitors
import pygame
from ToolTip import ToolTip
if platform.system == "Windows":
    os.environ['SDL_VIDEODRIVER'] = 'windib'
import pprint
pp = pprint.PrettyPrinter(indent=4)

# import pygame.display as display
# import time
# from pprint import pprint
# from graphics import *
colorList = []
currentColor = 'black'
screen = ''
screenWidth = 0
screenHeight = 0
monitorWidth = 0
monitorHeight = 0
screenPosVertical = -700
screenPosHorizontal = 900
root = 0

pygame.init()
pygame.display.init()

gettrace = getattr(sys, 'gettrace', None)
if gettrace is None:
    print('No sys.gettrace')
    debugMode = True
elif gettrace():
    print('Hmm, Big Debugger is watching me')
    debugMode = True
else:
    print("No debugger detected")
    debugMode = False
    if debugMode:
        print(' __name__', __name__)


class game:
    root = tkinter.Tk()
    drawThePointsCheckButton = tkinter.BooleanVar()
    drawPointConnectorsCheckButton = tkinter.BooleanVar()
    drawPointLinesCheckButton = tkinter.BooleanVar()
    numberOfCirclesVar = tkinter.IntVar()
    degreesBetweenPointsVar = tkinter.IntVar()
    circleRadiusVar = tkinter.IntVar()

    def main():
        global screen
        global screenWidth
        global screenHeight
        global monitorWidth
        global monitorHeight
        global root
        global screenPosVertical
        global screenPosHorizontal
        global debugMode
        menuWidth = 225
        menuHeight = 500
        # geometry = '100x300+100+-700'
        geometry = ''.join([str(menuWidth), "x",
                            str(menuHeight + 20), "+",
                            str(screenPosHorizontal - menuWidth - 10), "+",
                            str(screenPosVertical - 40)])

        game.root.geometry(geometry)
        game.root.title("Draw some circles")
        main_dialog = tkinter.Frame(root)
        main_dialog.pack(side=tkinter.TOP,
                         fill=tkinter.X)

        game.setUp()
        # #######################################
        quitButton = tkinter.Button(root,
                                    text="Quit",
                                    fg='blue',
                                    bg='white',
                                    width=30,
                                    command=game.quitProgram)
        quitButton.pack(side=tkinter.TOP,
                        fill=tkinter.X)
        ToolTip(quitButton, text='Quit the program')
        # #######################################
        drawCirclesButton = tkinter.Button(root,
                                           text="Draw",
                                           fg='blue',
                                           bg='white',
                                           width=30,
                                           command=game.drawTheCircles)
        drawCirclesButton.pack(side=tkinter.TOP,
                               fill=tkinter.X)
        ToolTip(drawCirclesButton, text='Draw some circles')
        # #######################################
        clearCirclesButton = tkinter.Button(root,
                                            text="Clear",
                                            fg='blue',
                                            bg='white',
                                            width=30,
                                            command=game.clearDisplay)
        clearCirclesButton.pack(side=tkinter.TOP,
                                fill=tkinter.X)
        ToolTip(clearCirclesButton, text='Clear the display')
        # #######################################
        clearAndDrawButton = tkinter.Button(root,
                                            text="Clear & Draw",
                                            fg='blue',
                                            bg='white',
                                            width=30,
                                            command=game.clearAndDrawTheCircles)
        clearAndDrawButton.pack(side=tkinter.TOP,
                                fill=tkinter.X)
        ToolTip(clearAndDrawButton, text='Clear display and draw circles')
        # #######################################
        selectScreenFillButton = tkinter.Button(root,
                                                text='Select Screen Fill',
                                                fg='blue',
                                                bg='white',
                                                width=30,
                                                command=game.selectScreenFill)
        selectScreenFillButton.pack(side=tkinter.TOP,
                                    fill=tkinter.X)
        ToolTip(selectScreenFillButton, text='Select a background color')
        # #######################################
        randomScreenFillButton = tkinter.Button(root,
                                                text='Random Screen Fill',
                                                fg='blue',
                                                bg='white',
                                                width=30,
                                                command=game.randomScreenFill)
        randomScreenFillButton.pack(side=tkinter.TOP,
                                    fill=tkinter.X)
        ToolTip(randomScreenFillButton, text='Random screen fill color')
        # #######################################
        checkButtonFrame = tkinter.Frame(root,
                                         bg='white',
                                         highlightbackground="black",
                                         relief=tkinter.RAISED)
        checkButtonFrame.pack(side=tkinter.TOP,
                              fill=tkinter.X)

        drawPointsCheckButton = tkinter.Checkbutton(checkButtonFrame,
                                                    text='Draw points',
                                                    fg='blue',
                                                    bg='white',
                                                    onvalue=True,
                                                    offvalue=False,
                                                    command=lambda: print('Draw points'),
                                                    variable=game.drawThePointsCheckButton)
        drawPointsCheckButton.pack(side=tkinter.TOP,
                                   fill=tkinter.X,
                                   anchor=tkinter.W)

        ToolTip(drawPointsCheckButton, 'Draw the circle points')
        game.drawThePointsCheckButton.set(True)
        # #######################################
        drawPointConnectorsCheckButton = tkinter.Checkbutton(checkButtonFrame,
                                                             text='Draw point connectors',
                                                             fg='blue',
                                                             bg='white',
                                                             onvalue=True,
                                                             offvalue=False,
                                                             command=lambda: print('Draw point connectors'),
                                                             variable=game.drawPointConnectorsCheckButton)
        drawPointConnectorsCheckButton.pack(side=tkinter.TOP,
                                            fill=tkinter.X,
                                            anchor=tkinter.W)

        ToolTip(drawPointConnectorsCheckButton, 'Draw connectors between points')
        game.drawPointConnectorsCheckButton.set(False)
        # #######################################
        drawPointLinesCheckButton = tkinter.Checkbutton(checkButtonFrame,
                                                        text='Draw point lines',
                                                        fg='blue',
                                                        bg='white',
                                                        onvalue=True,
                                                        offvalue=False,
                                                        command=lambda: print('Draw point lines'),
                                                        variable=game.drawPointLinesCheckButton)
        drawPointLinesCheckButton.pack(side=tkinter.TOP,
                                       fill=tkinter.X,
                                       anchor=tkinter.W)

        ToolTip(drawPointLinesCheckButton, text='Draw lines between circles')
        game.drawPointLinesCheckButton.set(False)
        # #######################################
        numberOfCirclesFrame = tkinter.Frame(root,
                                             bg='white',
                                             highlightbackground="black",
                                             relief=tkinter.RAISED)
        numberOfCirclesFrame.pack(side=tkinter.TOP,
                                  fill=tkinter.X)

        numberOfCircles = tkinter.Scale(numberOfCirclesFrame,
                                        fg='blue',
                                        bg='white',
                                        highlightcolor='red',
                                        label='Number of Circles',
                                        length=200,
                                        from_=2,
                                        to=20,
                                        variable=game.numberOfCirclesVar,
                                        orient=tkinter.HORIZONTAL)
        numberOfCircles.pack(side=tkinter.TOP,
                             fill=tkinter.X)
        ToolTip(numberOfCircles, 'Select number of circles to draw.')
        game.numberOfCirclesVar.set(2)

        # #######################################
        degreesBetweenPointsFrame = tkinter.Frame(root,
                                                  bg='white',
                                                  highlightbackground="black",
                                                  relief=tkinter.RAISED)
        degreesBetweenPointsFrame.pack(side=tkinter.TOP,
                                       fill=tkinter.X)

        degreesBetweenPoints = tkinter.Scale(degreesBetweenPointsFrame,
                                             fg='blue',
                                             bg='white',
                                             highlightcolor='red',
                                             label='Degrees between points',
                                             length=200,
                                             from_=2,
                                             to=180,
                                             resolution=2,
                                             variable=game.degreesBetweenPointsVar,
                                             orient=tkinter.HORIZONTAL)
        degreesBetweenPoints.pack(side=tkinter.TOP,
                                  fill=tkinter.X)

        ToolTip(degreesBetweenPoints, 'Select degrees between points.')
        game.degreesBetweenPointsVar.set(10)
        # #######################################
        circleRadiusFrame = tkinter.Frame(root,
                                          bg='white',
                                          highlightbackground="black",
                                          relief=tkinter.RAISED)
        circleRadiusFrame.pack(side=tkinter.TOP,
                               fill=tkinter.X)

        circleRadius = tkinter.Scale(circleRadiusFrame,
                                     fg='blue',
                                     bg='white',
                                     label='Circle radius',
                                     length=200,
                                     from_=2,
                                     to=20,
                                     variable=game.circleRadiusVar,
                                     orient=tkinter.HORIZONTAL)
        circleRadius.pack(side=tkinter.TOP,
                          fill=tkinter.X)

        ToolTip(circleRadius, 'Select circle radius.')
        game.circleRadiusVar.set(15)
        # #######################################

        tkinter.mainloop()

    def quitProgram():
        if debugMode:
            print("Quit using window X")
        pygame.display.quit
        pygame.quit()
        sys.exit(0)
    # #######################################

    def setUp():
        global debugMode
        global colorList
        global screen
        global screenWidth
        global screenHeight
        global monitorWidth
        global monitorHeight
        global root

        monitorInfo = get_monitors()
        if debugMode:
            print('setUp')
            for monitorInfo in get_monitors():
                print(str(monitorInfo))
        # monitorWidth = monitorInfo.width
        # monitorHeight = monitorInfo.height

        # screen position, size, and color
        screenPosVertical = -700
        screenPosHorizontal = 900
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%i, %i' % (screenPosHorizontal, screenPosVertical)
        screenWidth = 800
        screenHeight = 500
        # menuWidth = 150
        # menuHeight = screenHeight - 20
        screen = pygame.display.set_mode((screenWidth,
                                         screenHeight),
                                         pygame.RESIZABLE)
        pygame.display.set_caption("Draw some circles", "CIRCLES")
        pygame.event.pump()

        # Generate list of colors
        colorKeys = pygame.color.THECOLORS.keys()
        colorList = list(colorKeys)
        if debugMode:
            print("Number of colors: ", len(colorList))
        # erase the text file
        fileDebug = open("DougPyCircle.txt", "w")
        fileDebug.close()
    # #######################################
    # This generates all of the arrays needed
    # The following generates an array of points on a circle

    def getAllOfTheArrays():
        allPointsList = []

        def getACircleArray(horizontalPosition, verticalPosition):
            global debugMode
            if debugMode:
                print('getACircleArray')

            step = 0
            pointsList = []
            while (step < 2 * math.pi):  # about 6.28
                step += (0.01745329 * game.degreesBetweenPointsVar.get())
                x = game.circleRadiusVar.get() * math.cos(step) + horizontalPosition
                y = game.circleRadiusVar.get() * math.sin(step) + verticalPosition
                point = [round(x, ), round(y, 2)]
                pointsList.append(point)
            print('len(pointsList)', len(pointsList))
            return pointsList

        counter = game.numberOfCirclesVar.get()
        while counter > 0:
            counter -= 1
            horizontalPosition = random.randrange(0, screenWidth)
            verticalPosition = random.randrange(0, screenHeight)
            allPointsList.append(getACircleArray(horizontalPosition, verticalPosition))
            print('len(allPointsList', len(allPointsList))
        pass

    def drawThePoints(pointsList,
                      screen,
                      colorList):
        global debugMode
        if debugMode:
            print('drawThePoints')
        for aPoint in pointsList:
            currentColor = colorList[random.randrange(0, len(colorList))]
            pygame.draw.circle(screen,
                               currentColor,
                               (aPoint[0], aPoint[1]),
                               4,
                               4)

    def clearDisplay():
        global debugMode
        global colorList
        global currentColor
        screen.fill(currentColor)
        pygame.display.flip()
        if debugMode:
            print('clearDisplay: ', currentColor)

    def writeDebugFile(pointsList):
        global debugMode
        if debugMode:
            print('writeDebugFile')
        fileDebug = open("DougPyCircle.txt", "a")
        for a in pointsList:
            my = ' '.join([str(a[0]), '\t', str(a[1])])
            fileDebug.write(my + '\n')
        fileDebug.write('=' * 50 + '\n')
        fileDebug.close()

    def selectScreenFill():
        global debugMode
        global currentColor
        colors = askcolor(title="Color Chooser")
        if debugMode:
            print(colors[0], colors[1])
        if colors[0] is None:  # cancel was selected
            return
        currentColor = colors[1]
        screen.fill(currentColor)
        pygame.display.flip()
        if debugMode:
            print('selectScreenFill')

    def randomScreenFill():
        global debugMode
        global colorList
        global currentColor
        color = random.randrange(0, len(colorList))
        currentColor = colorList[color]
        screen.fill(currentColor)
        pygame.display.flip()
        if debugMode:
            print('Screen fill color: ', color, currentColor)

    def drawTheCircles():
        global debugMode
        if debugMode:
            print('drawTheCircles')
        game.getAllOfTheArrays()

    def clearAndDrawTheCircles():
        game.clearDisplay()
        game.drawTheCircles()

    # This is where we loop until user wants to exit
    # Fills screen with a random color


if __name__ == "__main__":
    game.main()
