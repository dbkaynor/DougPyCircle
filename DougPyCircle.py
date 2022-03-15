import math
import os
import platform
import random
import sys
import tkinter
from tkinter import messagebox
from tkinter.colorchooser import askcolor

import pygame
from screeninfo import get_monitors

from ToolTip import ToolTip

if platform.system() == "Windows":
    os.environ["SDL_VIDEODRIVER"] = "windib"
import pprint

debugMode = True
pp = pprint.PrettyPrinter(indent=4)
colorList = []
currentBackgroundColor = "black"
monitorWidth = 0
monitorHeight = 0

if platform.system() == "Windows":
    screenPosVertical = -900
    screenPosHorizontal = 250
elif platform.system() == "Linux":
    screenPosVertical = 0
    screenPosHorizontal = 250
else:
    print("Unknown platform " + platform.system())
    exit()

foregroundColor = "white"
root = 0

pygame.init()
pygame.display.init()
# https://www.pygame.org/docs/ref/event.html
for event in pygame.event.get():
    if event.type == pygame.WINDOWRESIZED:
        print('resize')
'''
gettrace = getattr(sys, "gettrace", None)
print(gettrace)
if gettrace is None:
    print("No sys.gettrace")
    debugMode = True
elif gettrace:
    print("Hmm, Big Debugger is watching me")
    debugMode = True
else:
    print("No debugger detected")
    debugMode = False
    if debugMode:
        print(" __name__", __name__)
'''

class circles:
    root = tkinter.Tk()
    clearBeforeDrawCheckButtonVar = tkinter.BooleanVar()
    drawThePointsCheckButtonVar = tkinter.BooleanVar()
    drawPointConnectorsCheckButtonVar = tkinter.BooleanVar()
    drawCircleConnectorsCheckButtonVar = tkinter.BooleanVar()
    foregroundColorRandomCheckButtonVar = tkinter.BooleanVar()
    backgroundColorRandomCheckButtonVar = tkinter.BooleanVar()
    twistedLinesCheckButtonVar = tkinter.BooleanVar()
    shiftedLinesCheckButtonVar = tkinter.BooleanVar()
    numberOfCirclesVar = tkinter.IntVar()
    degreesBetweenPointsVar = tkinter.IntVar()
    minimumCircleRadiusVar = tkinter.IntVar()
    maximumCircleRadiusVar = tkinter.IntVar()
    pointRadiusVar = tkinter.IntVar()
    lineThicknessVar = tkinter.IntVar()
    repeatCountVar = tkinter.IntVar()
    menuWidth = 220
    menuHeight = 800

    def main():
        global monitorWidth
        global monitorHeight
        global root
        global screenPosVertical
        global screenPosHorizontal
        global foregroundColor
        global debugMode

        pygame.event.pump()
        # event = pygame.event.wait()
        # print('event: ', str(event))

        geometry = "".join(
            [
                str(circles.menuWidth),
                "x",
                str(circles.menuHeight),
                "+",
                str(screenPosHorizontal - circles.menuWidth - 10),
                "+",
                str(screenPosVertical - 80),
            ]
        )

        circles.root.geometry(geometry)
        circles.root.resizable(height=False, width=False)
        circles.root.title("Draw some circles")
        main_dialog = tkinter.Frame(root)
        main_dialog.pack(side=tkinter.TOP, fill=tkinter.X)
        print("dirname:    ", os.path.dirname(__file__))
        photo = tkinter.PhotoImage(
            file="".join([os.path.dirname(__file__), os.sep, "KickUnderBus.png"])
        )
        circles.root.iconphoto(True, photo)

        circles.setUp()

        # #######################################
        drawCirclesButton = tkinter.Button(
            root,
            text="Draw",
            fg="blue",
            bg="white",
            width=20,
            command=circles.drawTheCircles,
        )
        drawCirclesButton.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(drawCirclesButton, text="Draw some circles")
        # #######################################
        clearCirclesButton = tkinter.Button(
            root,
            text="Clear",
            fg="blue",
            bg="white",
            width=20,
            command=circles.clearDisplay,
        )
        clearCirclesButton.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(clearCirclesButton, text="Clear the display")
        # #######################################
        selectScreenFillButton = tkinter.Button(
            root,
            text="Select background color",
            fg="blue",
            bg="white",
            width=20,
            command=circles.selectBackgroundColor,
        )
        selectScreenFillButton.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(selectScreenFillButton, text="Select background color")
        # #######################################
        randomScreenFillButton = tkinter.Button(
            root,
            text="Random background color",
            fg="blue",
            bg="white",
            width=20,
            command=circles.randomBackgroundColor,
        )
        randomScreenFillButton.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(randomScreenFillButton, text="Random  background color")
        # #######################################
        selectforegroundColorButton = tkinter.Button(
            root,
            text="Select foreground color",
            fg="blue",
            bg="white",
            width=20,
            command=circles.selectforegroundColor,
        )
        selectforegroundColorButton.pack(
            side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X
        )
        ToolTip(selectforegroundColorButton, text="Select foreground color")
        # #######################################
        checkButtonFrame = tkinter.Frame(
            root,
            bg="white",
            width=20,
            highlightbackground="black",
            relief=tkinter.RAISED
        )
        checkButtonFrame.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)

        clearBeforeDrawCheckButton = tkinter.Checkbutton(
            checkButtonFrame,
            text="Clear before draw",
            fg="blue",
            bg="white",
            onvalue=True,
            offvalue=False,
            command=lambda: print("Clear before draw"),
            variable=circles.clearBeforeDrawCheckButtonVar
        )
        clearBeforeDrawCheckButton.pack(side=tkinter.TOP, anchor=tkinter.W)
        circles.clearBeforeDrawCheckButtonVar.set(True)

        drawPointsCheckButton = tkinter.Checkbutton(
            checkButtonFrame,
            text="Draw circle points",
            fg="blue",
            bg="white",
            onvalue=True,
            offvalue=False,
            command=lambda: print("Draw points"),
            variable=circles.drawThePointsCheckButtonVar,
        )
        drawPointsCheckButton.pack(side=tkinter.TOP, anchor=tkinter.W)

        ToolTip(drawPointsCheckButton, "Draw the circle points")
        circles.drawThePointsCheckButtonVar.set(True)
        # #######################################
        drawPointConnectorsCheckButton = tkinter.Checkbutton(
            checkButtonFrame,
            text="Draw point connector lines",
            fg="blue",
            bg="white",
            onvalue=True,
            offvalue=False,
            command=lambda: print("Draw point connectors"),
            variable=circles.drawPointConnectorsCheckButtonVar,
        )
        drawPointConnectorsCheckButton.pack(side=tkinter.TOP, anchor=tkinter.W)

        ToolTip(drawPointConnectorsCheckButton, "Draw connectors between points")
        circles.drawPointConnectorsCheckButtonVar.set(True)
        # #######################################
        drawCircleConnectorsCheckButton = tkinter.Checkbutton(
            checkButtonFrame,
            text="Draw circle connector lines",
            fg="blue",
            bg="white",
            onvalue=True,
            offvalue=False,
            command=lambda: print("Draw circle connector lines"),
            variable=circles.drawCircleConnectorsCheckButtonVar,
        )
        # trunk-ignore(flake8/E501)
        drawCircleConnectorsCheckButton.pack(side=tkinter.TOP, anchor=tkinter.W)

        ToolTip(drawCircleConnectorsCheckButton, text="Draw lines between circles")
        circles.drawCircleConnectorsCheckButtonVar.set(True)
        # #######################################
        foregroundColorRandomCheckButton = tkinter.Checkbutton(
            checkButtonFrame,
            text="Random foreground color",
            fg="blue",
            bg="white",
            onvalue=True,
            offvalue=False,
            command=lambda: print("Random foreground color"),
            variable=circles.foregroundColorRandomCheckButtonVar,
        )
        foregroundColorRandomCheckButton.pack(side=tkinter.TOP, anchor=tkinter.W)

        ToolTip(foregroundColorRandomCheckButton, text="Random foreground color")
        circles.foregroundColorRandomCheckButtonVar.set(True)
        # #######################################
        backgroundColorRandomCheckButton = tkinter.Checkbutton(
            checkButtonFrame,
            text="Random background color",
            fg="blue",
            bg="white",
            onvalue=True,
            offvalue=False,
            command=lambda: print("Random background color"),
            variable=circles.backgroundColorRandomCheckButtonVar,
        )
        backgroundColorRandomCheckButton.pack(side=tkinter.TOP, anchor=tkinter.W)

        ToolTip(backgroundColorRandomCheckButton, text="Random background color")
        circles.backgroundColorRandomCheckButtonVar.set(False)
        # #######################################
        twistedCheckButton = tkinter.Checkbutton(
            checkButtonFrame,
            text="Twisted lines",
            fg="blue",
            bg="white",
            onvalue=True,
            offvalue=False,
            command=lambda: print("Twisted lines"),
            variable=circles.twistedLinesCheckButtonVar,
        )
        twistedCheckButton.pack(side=tkinter.TOP, anchor=tkinter.W)

        ToolTip(twistedCheckButton, text="Twisted lines")
        circles.twistedLinesCheckButtonVar.set(False)
        # #######################################
        shiftedLinesCheckButton = tkinter.Checkbutton(
            checkButtonFrame,
            text="Shifted lines",
            fg="blue",
            bg="white",
            onvalue=True,
            offvalue=False,
            command=lambda: print("Shifted lines"),
            variable=circles.shiftedLinesCheckButtonVar,
        )
        shiftedLinesCheckButton.pack(side=tkinter.TOP, anchor=tkinter.W)

        ToolTip(shiftedLinesCheckButton, text="Shiftedlines")
        circles.shiftedLinesCheckButtonVar.set(False)
        # #######################################
        numberOfCircles = tkinter.Scale(
            root,
            fg="blue",
            bg="white",
            highlightcolor="red",
            label="Number of Circles",
            length=150,
            from_=2,
            to=20,
            variable=circles.numberOfCirclesVar,
            orient=tkinter.HORIZONTAL,
            relief=tkinter.RAISED,
        )
        numberOfCircles.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(numberOfCircles, "Select number of circles to draw.")
        circles.numberOfCirclesVar.set(2)

        # #######################################
        degreesBetweenPoints = tkinter.Scale(
            root,
            fg="blue",
            bg="white",
            highlightcolor="red",
            label="Degrees between points",
            length=150,
            from_=2,
            to=180,
            resolution=2,
            variable=circles.degreesBetweenPointsVar,
            orient=tkinter.HORIZONTAL,
            relief=tkinter.RAISED,
        )
        degreesBetweenPoints.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)

        ToolTip(degreesBetweenPoints, "Select degrees between points.")
        circles.degreesBetweenPointsVar.set(10)
        # #######################################
        minimumCircleRadius = tkinter.Scale(
            root,
            fg="blue",
            bg="white",
            label="Minimum circle radius",
            length=150,
            from_=2,
            to=200,
            variable=circles.minimumCircleRadiusVar,
            orient=tkinter.HORIZONTAL,
            relief=tkinter.RAISED,
        )
        minimumCircleRadius.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)

        ToolTip(minimumCircleRadius, "Select minimum circle radius.")
        circles.minimumCircleRadiusVar.set(10)
        # #######################################
        maximumCircleRadius = tkinter.Scale(
            root,
            fg="blue",
            bg="white",
            label="Maximum circle radius",
            length=150,
            from_=3,
            to=201,
            variable=circles.maximumCircleRadiusVar,
            orient=tkinter.HORIZONTAL,
            relief=tkinter.RAISED,
        )
        maximumCircleRadius.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)

        ToolTip(maximumCircleRadius, "Select maximum circle radius.")
        circles.maximumCircleRadiusVar.set(200)
        # #######################################
        pointRadius = tkinter.Scale(
            root,
            fg="blue",
            bg="white",
            label="Point radius",
            length=150,
            from_=1,
            to=20,
            variable=circles.pointRadiusVar,
            orient=tkinter.HORIZONTAL,
            relief=tkinter.RAISED,
        )
        pointRadius.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)

        ToolTip(pointRadius, "Select circle radius.")
        circles.pointRadiusVar.set(2)
        # #######################################
        lineThickness = tkinter.Scale(
            root,
            fg="blue",
            bg="white",
            label="Line thickness",
            length=150,
            from_=1,
            to=20,
            variable=circles.lineThicknessVar,
            orient=tkinter.HORIZONTAL,
            relief=tkinter.RAISED,
        )
        lineThickness.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)

        ToolTip(lineThickness, "Select line thickness.")
        circles.lineThicknessVar.set(2)
        # #######################################
        repeatCount = tkinter.Scale(
            root,
            fg="blue",
            bg="white",
            label="Repeat count",
            length=150,
            from_=1,
            to=20,
            variable=circles.repeatCountVar,
            orient=tkinter.HORIZONTAL,
            relief=tkinter.RAISED,
        )
        repeatCount.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)

        ToolTip(repeatCount, "Select repeat count.")
        circles.repeatCountVar.set(1)

         # #######################################
        quitButton = tkinter.Button(
            root,
            text="Quit",
            fg="blue",
            bg="white",
            width=20,
            command=circles.quitProgram
        )
        quitButton.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(quitButton, text="Quit the program")
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

        global menuHeight

        global monitorWidth
        global monitorHeight
        global root

        debugFile = "DougPyCircle.txt"
        if os.path.exists(debugFile):
            os.remove(debugFile)

        os.environ["SDL_VIDEO_WINDOW_POS"] = "%i, %i" % (
            screenPosHorizontal,
            screenPosVertical,
        )
        screenWidth = 800
        screenHeight = circles.menuHeight  # 550

        screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
        pygame.display.set_caption("Draw some circles", "CIRCLES")
        event = pygame.event.pump()

        monitorInfo = get_monitors()
        if debugMode:
            print("setUp")
            for monitorInfo in get_monitors():
                print(str(monitorInfo))

        pp.pprint(screen.get_size())
        pp.pprint(pygame.display.Info())
        pp.pprint(str(event))

        img = pygame.image.load(
            "".join([os.path.dirname(__file__), os.sep, "KickUnderBus.png"])
        )

        pygame.display.set_icon(img)

        # Generate list of colors
        colorKeys = pygame.color.THECOLORS.keys()
        colorList = list(colorKeys)
        if debugMode:
            print("Number of colors: ", len(colorList))

    # #######################################
    # The following generates an array of points on the circles
    def getAllOfTheArrays():
        allPointsList = []

        def getCircleRadius():
            if debugMode:
                print("getCircleRadius")
            try:
                circleRadius = random.randint(
                    circles.minimumCircleRadiusVar.get(),
                    circles.maximumCircleRadiusVar.get())
                return circleRadius

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    "".join(
                        [
                            "Invalid radius range",
                            "\nRadius minimum must be\nsmaller than radius maximum",
                            "\n\n",
                            str(e),
                        ]
                    ),
                )
                return -1

        def getACircleArray(circleRadius, horizontalPosition, verticalPosition):
            global debugMode
            # circleRadius = getCircleRadius()
            step = 0
            pointsList = []
            while step < 2 * math.pi:  # about 6.28
                step += 0.01745329 * circles.degreesBetweenPointsVar.get()
                x = circleRadius * math.cos(step) + horizontalPosition
                y = circleRadius * math.sin(step) + verticalPosition
                point = [round(x, 2), round(y, 2)]
                pointsList.append(point)
            if debugMode:
                print("len(pointsList)", len(pointsList))
                pp.pprint(pointsList)
            return pointsList

        # Generates the required number of circles
        counter = circles.numberOfCirclesVar.get()
        while counter > 0:
            counter -= 1
            circleRadius = getCircleRadius()

            screenWidth, screenHeight = screen.get_size()
            horizontalPosition = random.randrange(circleRadius, screenWidth - circleRadius)
            verticalPosition = random.randrange(circleRadius, screenHeight - circleRadius)

            allPointsList.append(getACircleArray(circleRadius, horizontalPosition, verticalPosition))
            if allPointsList[0] == -1:  # An error occurred so abort
                break
        return allPointsList
    # end of def getAllOfTheArrays()
    # #######################################

    def drawTheCircles():
        global debugMode
        global allPointsList
        if debugMode:
            print("drawTheCircles")

        circles.screenWidth, circles.screenHeight = screen.get_size()

        for x in range(circles.repeatCountVar.get()):
            pygame.event.pump()
            event = pygame.event.wait()
            print('event: ', str(event))
            allPointsList = circles.getAllOfTheArrays()
            if allPointsList[0] == -1:  # An error occurred so abort
                messagebox.showerror(
                    "Error",
                    "An error with circles.getAllOfTheArrays\n"
                )
                return
            if circles.clearBeforeDrawCheckButtonVar.get():
                circles.clearDisplay()
            if circles.backgroundColorRandomCheckButtonVar.get():
                circles.randomBackgroundColor()
            if circles.drawThePointsCheckButtonVar.get():
                circles.drawThePoints()
            if circles.drawPointConnectorsCheckButtonVar.get():
                circles.drawPointConnectors()
            if circles.drawCircleConnectorsCheckButtonVar.get():
                circles.drawCircleConnectors()
            pygame.display.flip()
            if circles.repeatCountVar.get() != 1:
                pygame.time.wait(1000*3)
                # time.sleep(3)

    # Draw the points
    def drawThePoints():
        global debugMode
        if debugMode:
            print("drawThePoints")
        for circlePointsList in allPointsList:
            for aPoint in circlePointsList:
                if circles.foregroundColorRandomCheckButtonVar.get():
                    currentForegroundColor = colorList[
                        random.randrange(0, len(colorList))
                    ]
                else:
                    currentForegroundColor = foregroundColor
                pygame.draw.circle(
                    screen,
                    currentForegroundColor,
                    (aPoint[0], aPoint[1]),
                    circles.pointRadiusVar.get(),
                    circles.lineThicknessVar.get(),
                )

    def drawPointConnectors():
        if debugMode:
            print("drawPointConnectors")
            pp.pprint(allPointsList)
        for circlePointsList in allPointsList:
            if circles.foregroundColorRandomCheckButtonVar.get():
                currentForegroundColor = colorList[random.randrange(0, len(colorList))]
            else:
                currentForegroundColor = foregroundColor

            for p1, p2 in zip(circlePointsList, circlePointsList[1:]):
                pygame.draw.line(
                    screen, currentForegroundColor, p1, p2, circles.lineThicknessVar.get()
                )

    # Draw connectors between points on the circumference of a circle
    def drawCircleConnectors():
        if debugMode:
            print("drawCircleConnectors")
            pp.pprint(allPointsList)

        # The first while loop is for all of the circles
        i = 0
        while i < len(allPointsList) - 1:
            if circles.twistedLinesCheckButtonVar.get():
                random.shuffle(allPointsList[i])
            if circles.shiftedLinesCheckButtonVar.get():
                count = random.randint(0, len(allPointsList[i]) - 1)
                print(count, len(allPointsList[i]))
                while count > 0:
                    count -= 1
                    allPointsList[i].append(allPointsList[i].pop(0))

            p1 = allPointsList[i]
            # pp.pprint(p1)
            i += 1
            p2 = allPointsList[i]
            # pp.pprint(p2)

            j = 0
            # This while loop is for the points in a circle
            while j < len(p1):
                for circlePointsList in allPointsList:
                    if circles.foregroundColorRandomCheckButtonVar.get():
                        currentForegroundColor = colorList[random.randrange(0, len(colorList))]
                    else:
                        currentForegroundColor = foregroundColor
                pygame.draw.line(screen, currentForegroundColor,

                                 p1[j], p2[j], circles.lineThicknessVar.get())
                j += 1

    def clearDisplay():
        global debugMode
        global colorList
        global currentBackgroundColor
        screen.fill(currentBackgroundColor)
        pygame.display.flip()
        if debugMode:
            print("clearDisplay: ", currentBackgroundColor)

    def writeDebugFile(pointsList):
        global debugMode
        if debugMode:
            print("writeDebugFile")
            fileDebug = open("DougPyCircle.txt", "a")
            for a in pointsList:
                my = " ".join([str(a[0]), "\t", str(a[1])])
                fileDebug.write(my + "\n")
            fileDebug.write("=" * 50 + "\n")
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
            print("selectBackgroundColor")

    def selectforegroundColor():
        global debugMode
        global foregroundColor
        colors = askcolor(title="Foreground color chooser")
        if debugMode:
            print(colors[0], colors[1])
        if colors[0] is None:  # cancel was selected
            return
        foregroundColor = colors[1]
        pygame.display.flip()
        if debugMode:
            print("selectforegroundColor")

    def randomBackgroundColor():
        global debugMode
        global colorList
        global currentBackgroundColor
        color = random.randrange(0, len(colorList))
        currentBackgroundColor = colorList[color]
        screen.fill(currentBackgroundColor)
        pygame.display.flip()
        if debugMode:
            print("randomBackgroundColor: ", color, currentBackgroundColor)

    # This is where we loop until user wants to exit

if __name__ == "__main__":
    circles.main()
