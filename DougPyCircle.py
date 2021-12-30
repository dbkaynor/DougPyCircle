# flake8 --extend-ignore=E501 "%f"
# https://sites.cs.ucsb.edu/~pconrad/cs5nm/topics/pygame/drawing/
# http://cs.roanoke.edu/Fall2013/CPSC120A/pygame-1.9.1-docs-html/ref/examples.html
# https://www.geeksforgeeks.org/creating-start-menu-in-pygame/
# https://www.pygame.org/docs/ref/draw.html
import math
import os
import platform
import random
import sys
import tkinter
from tkinter.colorchooser import askcolor
from tkinter import messagebox
from screeninfo import get_monitors
import pygame
from ToolTip import ToolTip
if platform.system() == "Windows":
    os.environ['SDL_VIDEODRIVER'] = 'windib'
import pprint
pp = pprint.PrettyPrinter(indent=4)
# import cv2
# import pygame.display as display
# import time
colorList = []
currentBackgroundColor = 'black'
screen = ''
screenWidth = 0
screenHeight = 0
monitorWidth = 0
monitorHeight = 0
if platform.system() == 'Windows':
    screenPosVertical = -750
    screenPosHorizontal = 250
elif platform.system() == 'Linux':
    screenPosVertical = 0
    screenPosHorizontal = 250
else:
    print('Unknown platform ' + platform.system())
    exit()

foregroundColor = 'white'
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
    drawThePointsCheckButtonVar = tkinter.BooleanVar()
    drawPointConnectorsCheckButtonVar = tkinter.BooleanVar()
    drawCircleConnectorsCheckButtonVar = tkinter.BooleanVar()
    foregroundColorRandomCheckButtonVar = tkinter.BooleanVar()
    numberOfCirclesVar = tkinter.IntVar()
    degreesBetweenPointsVar = tkinter.IntVar()
    minimumCircleRadiusVar = tkinter.IntVar()
    maximumCircleRadiusVar = tkinter.IntVar()
    pointRadiusVar = tkinter.IntVar()
    lineThicknessVar = tkinter.IntVar()
    menuWidth = 200
    menuHeight = 700

    def main():
        global screen
        global screenWidth
        global screenHeight
        global monitorWidth
        global monitorHeight
        global root
        global screenPosVertical
        global screenPosHorizontal
        global foregroundColor
        global debugMode

        geometry = ''.join([str(game.menuWidth), "x",
                            str(game.menuHeight), "+",
                            str(screenPosHorizontal - game.menuWidth - 10), "+",
                            str(screenPosVertical - 40)])

        game.root.geometry(geometry)
        game.root.resizable(height=False, width=False)
        game.root.title("Draw some circles")
        main_dialog = tkinter.Frame(root)
        main_dialog.pack(side=tkinter.TOP,
                         fill=tkinter.X)
        print('dirname:    ', os.path.dirname(__file__))
        photo = tkinter.PhotoImage(file=''.join([os.path.dirname(__file__),
                                                 os.sep,
                                                 'KickUnderBus.png']))
        game.root.iconphoto(True, photo)

        game.setUp()
        # #######################################
        quitButton = tkinter.Button(root,
                                    text="Quit",
                                    fg='blue',
                                    bg='white',
                                    width=20,
                                    command=game.quitProgram)
        quitButton.pack(side=tkinter.TOP,
                        anchor=tkinter.W,
                        fill=tkinter.X)
        ToolTip(quitButton, text='Quit the program')
        # #######################################
        drawCirclesButton = tkinter.Button(root,
                                           text="Draw",
                                           fg='blue',
                                           bg='white',
                                           width=20,
                                           command=game.drawTheCircles)
        drawCirclesButton.pack(side=tkinter.TOP,
                               anchor=tkinter.W,
                               fill=tkinter.X)
        ToolTip(drawCirclesButton, text='Draw some circles')
        # #######################################
        clearCirclesButton = tkinter.Button(root,
                                            text="Clear",
                                            fg='blue',
                                            bg='white',
                                            width=20,
                                            command=game.clearDisplay)
        clearCirclesButton.pack(side=tkinter.TOP,
                                anchor=tkinter.W,
                                fill=tkinter.X)
        ToolTip(clearCirclesButton, text='Clear the display')
        # #######################################
        clearAndDrawButton = tkinter.Button(root,
                                            text="Clear & Draw",
                                            fg='blue',
                                            bg='white',
                                            width=20,
                                            command=game.clearAndDrawTheCircles)
        clearAndDrawButton.pack(side=tkinter.TOP,
                                anchor=tkinter.W,
                                fill=tkinter.X)
        ToolTip(clearAndDrawButton, text='Clear display and draw circles')
        # #######################################
        selectScreenFillButton = tkinter.Button(root,
                                                text='Select background color',
                                                fg='blue',
                                                bg='white',
                                                width=20,
                                                command=game.selectBackgroundColor)
        selectScreenFillButton.pack(side=tkinter.TOP,
                                    anchor=tkinter.W,
                                    fill=tkinter.X)
        ToolTip(selectScreenFillButton, text='Select background color')
        # #######################################
        randomScreenFillButton = tkinter.Button(root,
                                                text='Random background color',
                                                fg='blue',
                                                bg='white',
                                                width=20,
                                                command=game.randomBackgroundColor)
        randomScreenFillButton.pack(side=tkinter.TOP,
                                    anchor=tkinter.W,
                                    fill=tkinter.X)
        ToolTip(randomScreenFillButton, text='Random  background color')
        # #######################################
        selectforegroundColorButton = tkinter.Button(root,
                                                     text='Select foreground color',
                                                     fg='blue',
                                                     bg='white',
                                                     width=20,
                                                     command=game.selectforegroundColor)
        selectforegroundColorButton.pack(side=tkinter.TOP,
                                         anchor=tkinter.W,
                                         fill=tkinter.X)
        ToolTip(selectforegroundColorButton, text='Select foreground color')
        # #######################################
        checkButtonFrame = tkinter.Frame(root,
                                         bg='white',
                                         width=20,
                                         highlightbackground="black",
                                         relief=tkinter.RAISED)
        checkButtonFrame.pack(side=tkinter.TOP,
                              anchor=tkinter.W,
                              fill=tkinter.X)

        drawPointsCheckButton = tkinter.Checkbutton(checkButtonFrame,
                                                    text='Draw points',
                                                    fg='blue',
                                                    bg='white',
                                                    onvalue=True,
                                                    offvalue=False,
                                                    command=lambda: print('Draw points'),
                                                    variable=game.drawThePointsCheckButtonVar)
        drawPointsCheckButton.pack(side=tkinter.TOP,
                                   anchor=tkinter.W)

        ToolTip(drawPointsCheckButton, 'Draw the circle points')
        game.drawThePointsCheckButtonVar.set(True)
        # #######################################
        drawPointConnectorsCheckButton = tkinter.Checkbutton(checkButtonFrame,
                                                             text='Draw point connectors',
                                                             fg='blue',
                                                             bg='white',
                                                             onvalue=True,
                                                             offvalue=False,
                                                             command=lambda: print('Draw point connectors'),
                                                             variable=game.drawPointConnectorsCheckButtonVar)
        drawPointConnectorsCheckButton.pack(side=tkinter.TOP,
                                            anchor=tkinter.W)

        ToolTip(drawPointConnectorsCheckButton, 'Draw connectors between points')
        game.drawPointConnectorsCheckButtonVar.set(True)
        # #######################################
        drawCircleConnectorsCheckButton = tkinter.Checkbutton(checkButtonFrame,
                                                              text='Draw point lines',
                                                              fg='blue',
                                                              bg='white',
                                                              onvalue=True,
                                                              offvalue=False,
                                                              command=lambda: print('Draw circle connector lines'),
                                                              variable=game.drawCircleConnectorsCheckButtonVar)
        drawCircleConnectorsCheckButton.pack(side=tkinter.TOP,
                                             anchor=tkinter.W)

        ToolTip(drawCircleConnectorsCheckButton, text='Draw lines between circles')
        game.drawCircleConnectorsCheckButtonVar.set(False)
        # #######################################
        foregroundColorRandomCheckButton = tkinter.Checkbutton(checkButtonFrame,
                                                               text='Random foreground color',
                                                               fg='blue',
                                                               bg='white',
                                                               onvalue=True,
                                                               offvalue=False,
                                                               command=lambda: print('Random foreground color'),
                                                               variable=game.foregroundColorRandomCheckButtonVar)
        foregroundColorRandomCheckButton.pack(side=tkinter.TOP,
                                              anchor=tkinter.W)

        ToolTip(foregroundColorRandomCheckButton, text='Random foreground color')
        game.foregroundColorRandomCheckButtonVar.set(False)
        # #######################################
        numberOfCircles = tkinter.Scale(root,
                                        fg='blue',
                                        bg='white',
                                        highlightcolor='red',
                                        label='Number of Circles',
                                        length=150,
                                        from_=2,
                                        to=20,
                                        variable=game.numberOfCirclesVar,
                                        orient=tkinter.HORIZONTAL,
                                        relief=tkinter.RAISED)
        numberOfCircles.pack(side=tkinter.TOP,
                             anchor=tkinter.W,
                             fill=tkinter.X)
        ToolTip(numberOfCircles, 'Select number of circles to draw.')
        game.numberOfCirclesVar.set(2)

        # #######################################
        degreesBetweenPoints = tkinter.Scale(root,
                                             fg='blue',
                                             bg='white',
                                             highlightcolor='red',
                                             label='Degrees between points',
                                             length=150,
                                             from_=2,
                                             to=180,
                                             resolution=2,
                                             variable=game.degreesBetweenPointsVar,
                                             orient=tkinter.HORIZONTAL,
                                             relief=tkinter.RAISED)
        degreesBetweenPoints.pack(side=tkinter.TOP,
                                  anchor=tkinter.W,
                                  fill=tkinter.X)

        ToolTip(degreesBetweenPoints, 'Select degrees between points.')
        game.degreesBetweenPointsVar.set(20)
        # #######################################
        minimumCircleRadius = tkinter.Scale(root,
                                            fg='blue',
                                            bg='white',
                                            label='Minimum circle radius',
                                            length=150,
                                            from_=2,
                                            to=200,
                                            variable=game. minimumCircleRadiusVar,
                                            orient=tkinter.HORIZONTAL,
                                            relief=tkinter.RAISED)
        minimumCircleRadius.pack(side=tkinter.TOP,
                                 anchor=tkinter.W,
                                 fill=tkinter.X)

        ToolTip(minimumCircleRadius, 'Select minimum circle radius.')
        game.minimumCircleRadiusVar.set(100)
        # #######################################
        maximumCircleRadius = tkinter.Scale(root,
                                            fg='blue',
                                            bg='white',
                                            label='Maximum circle radius',
                                            length=150,
                                            from_=2,
                                            to=200,
                                            variable=game.maximumCircleRadiusVar,
                                            orient=tkinter.HORIZONTAL,
                                            relief=tkinter.RAISED)
        maximumCircleRadius.pack(side=tkinter.TOP,
                                 anchor=tkinter.W,
                                 fill=tkinter.X)

        ToolTip(maximumCircleRadius, 'Select maximum circle radius.')
        game.maximumCircleRadiusVar.set(101)
        # #######################################
        pointRadius = tkinter.Scale(root,
                                    fg='blue',
                                    bg='white',
                                    label='Point radius',
                                    length=150,
                                    from_=1,
                                    to=20,
                                    variable=game.pointRadiusVar,
                                    orient=tkinter.HORIZONTAL,
                                    relief=tkinter.RAISED)
        pointRadius.pack(side=tkinter.TOP,
                         anchor=tkinter.W,
                         fill=tkinter.X)

        ToolTip(pointRadius, 'Select circle radius.')
        game.pointRadiusVar.set(2)
        # #######################################
        lineThickness = tkinter.Scale(root,
                                      fg='blue',
                                      bg='white',
                                      label='Line thickness',
                                      length=150,
                                      from_=1,
                                      to=20,
                                      variable=game.lineThicknessVar,
                                      orient=tkinter.HORIZONTAL,
                                      relief=tkinter.RAISED)
        lineThickness.pack(side=tkinter.TOP,
                           anchor=tkinter.W,
                           fill=tkinter.X)

        ToolTip(lineThickness, 'Select line thickness.')
        game.lineThicknessVar.set(2)
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
        global menuHeight

        global monitorWidth
        global monitorHeight
        global root

        debugFile = "DougPyCircle.txt"
        if os.path.exists(debugFile):
            os.remove(debugFile)

        monitorInfo = get_monitors()
        if debugMode:
            print('setUp')
            for monitorInfo in get_monitors():
                print(str(monitorInfo))
        # monitorWidth = monitorInfo.width
        # monitorHeight = monitorInfo.height

        # menuWidth = 150
        # menuHeight = 600
        # global screenPosVertical
        # global screenPosHorizontal

        # screen position, size, and color
        # screenPosVertical = -700
        # screenPosHorizontal = 500
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%i, %i' % (screenPosHorizontal, screenPosVertical)
        screenWidth = 800
        screenHeight = game.menuHeight  # 550
        # menuWidth = 150
        # menuHeight = screenHeight - 20
        screen = pygame.display.set_mode((screenWidth,
                                         screenHeight),
                                         pygame.RESIZABLE)
        pygame.display.set_caption("Draw some circles", "CIRCLES")
        pygame.event.pump()

        img = pygame.image.load(''.join([os.path.dirname(__file__),
                                         os.sep,
                                         'KickUnderBus.png']))

        pygame.display.set_icon(img)

        # Generate list of colors
        colorKeys = pygame.color.THECOLORS.keys()
        colorList = list(colorKeys)
        if debugMode:
            print("Number of colors: ", len(colorList))
            # erase the text file

    # #######################################
    # The following generates an array of points on the circles

    def getAllOfTheArrays():
        allPointsList = []

        def getACircleArray(horizontalPosition, verticalPosition):
            global debugMode
            if debugMode:
                print('getACircleArray')
            try:
                radius = random.randint(game.minimumCircleRadiusVar.get(),
                                        game.maximumCircleRadiusVar.get())
            except Exception as e:
                messagebox.showerror('Oppsie',
                                     ''.join([str(e),
                                              '\nInvalid radius range',
                                              '\nMinimum must be smaller than maximum']))
                return(-1)

            step = 0
            pointsList = []
            while (step < 2 * math.pi):  # about 6.28
                step += (0.01745329 * game.degreesBetweenPointsVar.get())
                x = radius * math.cos(step) + horizontalPosition
                y = radius * math.sin(step) + verticalPosition
                point = [round(x, 2), round(y, 2)]
                pointsList.append(point)
            if debugMode:
                print('len(pointsList)', len(pointsList))
                pp.pprint(pointsList)
            return pointsList

        counter = game.numberOfCirclesVar.get()
        while counter > 0:
            counter -= 1
            horizontalPosition = random.randrange(0, screenWidth)
            verticalPosition = random.randrange(0, screenHeight)
            allPointsList.append(getACircleArray(horizontalPosition, verticalPosition))
            print('len(allPointsList)', len(allPointsList))
            print('allPointsList[0]', allPointsList[0])
            if allPointsList[0] == -1:  # An error occurred so abort
                break
        return allPointsList

    def drawTheCircles():
        global debugMode
        global allPointsList
        if debugMode:
            print('drawTheCircles')
        allPointsList = game.getAllOfTheArrays()
        if allPointsList[0] == -1:  # An error occurred so abort
            return
        if game.drawThePointsCheckButtonVar.get():
            game.drawThePoints()
        if game.drawPointConnectorsCheckButtonVar.get():
            game.drawPointConnectors()
        if game.foregroundColorRandomCheckButtonVar.get():
            game.drawCircleConnectors()

    # Draw the points
    def drawThePoints():
        global debugMode
        if debugMode:
            print('drawThePoints')
        for circlePointsList in allPointsList:
            for aPoint in circlePointsList:
                if game.foregroundColorRandomCheckButtonVar.get():
                    currentForegroundColor = colorList[random.randrange(0, len(colorList))]
                else:
                    currentForegroundColor = foregroundColor
                pygame.draw.circle(screen,
                                   currentForegroundColor,
                                   (aPoint[0],
                                    aPoint[1]),
                                   game.pointRadiusVar.get(),
                                   game.lineThicknessVar.get())
        pygame.display.flip()

    def drawPointConnectors():
        if debugMode:
            print('drawPointConnectors')
        # pp.pprint(allPointsList)
        for circlePointsList in allPointsList:
            if game.foregroundColorRandomCheckButtonVar.get():
                currentForegroundColor = colorList[random.randrange(0, len(colorList))]
            else:
                currentForegroundColor = foregroundColor

            for p1, p2 in zip(circlePointsList, circlePointsList[1:]):
                pygame.draw.line(screen,
                                 currentForegroundColor,
                                 p1,
                                 p2,
                                 game.lineThicknessVar.get())
            pygame.display.flip()
        pass

# Draw connectors between points on the circumference of a circle
# Best way to shift a list in Python?
# https://stackoverflow.com/questions/44501591/best-way-to-shift-a-list-in-python
# Python Random shuffle() Method
# https://www.w3schools.com/python/ref_random_shuffle.asp
    # Connect points of two circles
    def drawCircleConnectors():
        if debugMode:
            print('drawCircleConnectors')
        # pp.pprint(allPointsList)
        for circlePointsList in allPointsList:
            for aPoint in circlePointsList:
                pp.pprint(aPoint)
                pass

    def clearAndDrawTheCircles():
        game.clearDisplay()
        game.drawTheCircles()

    def clearDisplay():
        global debugMode
        global colorList
        global currentBackgroundColor
        screen.fill(currentBackgroundColor)
        pygame.display.flip()
        if debugMode:
            print('clearDisplay: ', currentBackgroundColor)

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

    def selectBackgroundColor():
        global debugMode
        global currentBackgroundColor
        colors = askcolor(title="Background color chooser")
        if debugMode:
            print(colors[0], colors[1])
        if colors[0] is None:  # cancel was selected
            return
        currentBackgroundColor = colors[1]
        screen.fill(currentBackgroundColor)
        pygame.display.flip()
        if debugMode:
            print('selectBackgroundColor')

    def selectforegroundColor():
        global debugMode
        global foregroundColor
        colors = askcolor(title="Foreground color chooser")
        if debugMode:
            print(colors[0], colors[1])
        if colors[0] is None:  # cancel was selected
            return
        foregroundColor = colors[1]
        if debugMode:
            print('selectforegroundColor')

    def randomBackgroundColor():
        global debugMode
        global colorList
        global currentBackgroundColor
        color = random.randrange(0, len(colorList))
        currentBackgroundColor = colorList[color]
        screen.fill(currentBackgroundColor)
        pygame.display.flip()
        if debugMode:
            print('randomBackgroundColor: ', color, currentBackgroundColor)

    # This is where we loop until user wants to exit
    # Fills screen with a random color


if __name__ == "__main__":
    game.main()
