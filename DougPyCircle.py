# DougPyCircles.py
#
# Produces interesting patterns
#
# This  program  is free software: you can redistribute it and/or  modify it
# under the terms of the GNU General Public License as published by the Free
# Software  Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This  program  is  distributed  in the hope that it will  be  useful,  but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public  License
# for more details.
#
# You  should  have received a copy of the GNU General Public License  along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
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
import inspect
import pprint

# Clear the terminal at program startup
os.system('cls||clear')
pp = pprint.PrettyPrinter(indent=4)

StartUpDirectory = os.path.split(sys.argv[0])[0]
# HelpFileVar.set(os.path.join(StartUpDirectoryVar.get(), 'DougPyCircles.hlp'))

debugFile = os.path.join(StartUpDirectory, "DougPyCircles.txt")
if os.path.exists(debugFile):
    os.remove(debugFile)


def line_info(message="nothing", show=False):
    f = inspect.currentframe()
    i = inspect.getframeinfo(f.f_back)
    tString = f"{os.path.basename(i.filename)}:{i.lineno}  called from {i.function}  {message}\n"
    file1 = open(debugFile, "a")
    file1.write(tString)
    file1.close()
    if show:
        line_info(tString)


if platform.system() == "Windows":
    os.environ["SDL_VIDEODRIVER"] = "windib"

# This positioning is for testing purposes
if os.getenv("COMPUTERNAME") == 'DBKAYNOX-MOBL4':
    screenPosVertical = -1100
    screenPosHorizontal = 250
elif platform.system() == "Linux":
    screenPosVertical = 0
    screenPosHorizontal = 250
elif platform.system() == "OS X":
    screenPosVertical = 0
    screenPosHorizontal = 0
else:
    line_info(' '.join(["Unknown platform:", platform.system()]))
    exit()

screen = 0
tkRoot = 0
pygame.init()
pygame.display.init()

gettrace = getattr(sys, "gettrace", None)
line_info(gettrace)
line_info(' '.join([" __name__", __name__]))


def about():
    messagebox.showinfo('About DougPyCircle',
                        os.linesep.join([' '.join(['Start directory: ',
                                                   os.getcwd()]),
                                         ' '.join(['Script name:',
                                                   os.path.basename(__file__)]),
                                         ' '.join(['Version:',
                                                   str(os.path.getmtime(__file__))]),
                                         ' '.join(['Geometry:',
                                                   tkRoot.geometry()]),
                                         ' '.join(['Screen size:',
                                                   str(tkRoot.winfo_screenwidth()),
                                                   'x',
                                                   str(tkRoot.winfo_screenheight())]),
                                         ' '.join(['Python version:',
                                                   platform.python_version()]),
                                         ' '.join(['Platform:',
                                                   platform.platform()])
                                         ]))


class circles:
    global tkRoot
    tkRoot = tkinter.Tk()
    clearBeforeDrawCheckButtonVar = tkinter.BooleanVar()
    drawThePointsCheckButtonVar = tkinter.BooleanVar()
    drawPointConnectorsCheckButtonVar = tkinter.BooleanVar()
    drawCircleConnectorsCheckButtonVar = tkinter.BooleanVar()
    foregroundColorRandomCheckButtonVar = tkinter.BooleanVar()
    backgroundColorRandomCheckButtonVar = tkinter.BooleanVar()
    twistedLinesCheckButtonVar = tkinter.BooleanVar()
    shiftedLinesVar = tkinter.IntVar()
    numberOfCirclesVar = tkinter.IntVar()
    degreesBetweenPointsVar = tkinter.IntVar()
    minimumCircleRadiusVar = tkinter.IntVar()
    maximumCircleRadiusVar = tkinter.IntVar()
    pointRadiusVar = tkinter.IntVar()
    lineThicknessVar = tkinter.IntVar()
    repeatCountVar = tkinter.IntVar()
    repeatDelayVar = tkinter.IntVar()
    menuWidth = 220
    menuHeight = 900
    colorList = []
    foregroundColor = "white"
    backgroundColor = "black"

    # https://www.pygame.org/docs/ref/event.html
    for event in pygame.event.get():
        if event.type == pygame.WINDOWRESIZED:
            line_info('resize')

    def main():
        global tkRoot
        global screenPosVertical
        global screenPosHorizontal

        pygame.event.pump()
        # event = pygame.event.wait()
        # line_info('event: ', str(event))

        geometry = "".join(
            [
                str(circles.menuWidth),
                "x",
                str(circles.menuHeight),
                "+",
                str(screenPosHorizontal - circles.menuWidth - 10),
                "+",
                str(screenPosVertical),
            ]
        )

        tkRoot.geometry(geometry)
        tkRoot.resizable(height=False, width=False)
        tkRoot.title("Draw some circles")
        main_dialog = tkinter.Frame(tkRoot)
        main_dialog.pack(side=tkinter.TOP, fill=tkinter.X)
        line_info("dirname:    ", os.path.dirname(__file__))
        photo = tkinter.PhotoImage(
            file="".join([os.path.dirname(__file__), os.sep, "KickUnderBus.png"])
        )
        tkRoot.iconphoto(True, photo)

        circles.setUp()

        # #######################################
        drawCirclesButton = tkinter.Button(
            tkRoot,
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
            tkRoot,
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
            tkRoot,
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
            tkRoot,
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
            tkRoot,
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
            tkRoot,
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
            command=lambda: line_info("Clear before draw"),
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
            command=lambda: line_info("Draw points"),
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
            command=lambda: line_info("Draw point connectors"),
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
            command=lambda: line_info("Draw circle connector lines"),
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
            command=lambda: line_info("Random foreground color"),
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
            command=lambda: line_info("Random background color"),
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
            command=lambda: line_info("Twisted lines"),
            variable=circles.twistedLinesCheckButtonVar,
        )
        twistedCheckButton.pack(side=tkinter.TOP, anchor=tkinter.W)

        ToolTip(twistedCheckButton, text="Twisted lines")
        circles.twistedLinesCheckButtonVar.set(False)
        # #######################################
        shiftedLines = tkinter.Scale(
            tkRoot,
            fg="blue",
            bg="white",
            highlightcolor="red",
            label="Shifted lines",
            length=150,
            from_=-1,
            to=20,
            variable=circles.shiftedLinesVar,
            orient=tkinter.HORIZONTAL,
            relief=tkinter.RAISED,
        )
        shiftedLines.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(shiftedLines, text="Shifted lines")
        circles.shiftedLinesVar.set(0)
        # #######################################
        numberOfCircles = tkinter.Scale(
            tkRoot,
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
            tkRoot,
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
            tkRoot,
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
            tkRoot,
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
            tkRoot,
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
            tkRoot,
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
            tkRoot,
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
        repeatDelay = tkinter.Scale(
            tkRoot,
            fg="blue",
            bg="white",
            label="Repeat delay",
            length=150,
            from_=1,
            to=20,
            variable=circles.repeatDelayVar,
            orient=tkinter.HORIZONTAL,
            relief=tkinter.RAISED,
        )
        repeatDelay.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)

        ToolTip(repeatDelay, "Select repeat delay.")
        circles.repeatDelayVar.set(3)
        # #######################################
        quitButton = tkinter.Button(
            tkRoot,
            text="Quit",
            fg="blue",
            bg="white",
            width=20,
            command=circles.quitProgram
        )
        quitButton.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(quitButton, text="Quit the program")
        # #######################################
        aboutButton = tkinter.Button(
            tkRoot,
            text="About",
            fg="blue",
            bg="white",
            width=20,
            command=about
        )
        aboutButton.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(aboutButton, text="About the program")

        # #######################################
        tkRoot.after(1000, circles.clearDisplay)
        tkRoot.mainloop()

    def quitProgram():
        line_info("Quit using window X")
        pygame.display.quit
        pygame.quit()
        sys.exit(0)

    # #######################################

    def setUp():
        # circles.colorList
        global screen
        global menuHeight

        os.environ["SDL_VIDEO_WINDOW_POS"] = "%i, %i" % (
            screenPosHorizontal,
            screenPosVertical
        )
        screenWidth = 800
        screenHeight = circles.menuHeight + 50  # 550

        screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.NOFRAME)
        pygame.display.set_caption("Draw some circles", "CIRCLES")
        pygame.event.pump()

        monitorInfo = get_monitors()
        line_info("setUp")
        for monitorInfo in get_monitors():
            line_info(str(monitorInfo))

        pp.pprint(screen.get_size())
        pp.pprint(pygame.display.Info())
        pp.pprint(str(circles.event))

        img = pygame.image.load(
            "".join([os.path.dirname(__file__), os.sep, "KickUnderBus.png"])
        )

        pygame.display.set_icon(img)

        # Generate list of colors
        colorKeys = pygame.color.THECOLORS.keys()
        circles.colorList = list(colorKeys)
        line_info(' '.join(["Number of colors:", str(len(circles.colorList))]))

    # #######################################
    # The following generates an array of points on the circles
    def getAllOfTheArrays():
        allPointsList = []

        def getCircleRadius():
            line_info("getCircleRadius")
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
            step = 0
            pointsList = []
            while step < 2 * math.pi:  # about 6.28
                step += 0.01745329 * circles.degreesBetweenPointsVar.get()
                x = circleRadius * math.cos(step) + horizontalPosition
                y = circleRadius * math.sin(step) + verticalPosition
                point = [round(x, 2), round(y, 2)]
                pointsList.append(point)
            line_info(' '.join(['len(pointsList)', str(len(pointsList))]))
            # pp.pprint(pointsList)
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

    def drawScreenText(infoString, virtualScreenWidth, virtualScreenHeight):
        infoFont = pygame.font.SysFont('Verdana', 20)

        fontColor = 'pink'
        infoText = infoFont.render(infoString, True, fontColor)
        fgText = infoFont.render(circles.foregroundColor, True, fontColor)
        bgText = infoFont.render(circles.backgroundColor, True, fontColor)
        size = ' '.join([str(virtualScreenWidth), str(virtualScreenHeight)])
        sizeText = infoFont.render(size, True, fontColor)

        screen.blit(infoText, (virtualScreenWidth / 2 - 35, virtualScreenHeight / 2 - 10))
        screen.blit(bgText, (virtualScreenWidth / 2 - 35, virtualScreenHeight / 2 - 35))
        screen.blit(fgText, (virtualScreenWidth / 2 - 35, virtualScreenHeight / 2 - 60))
        screen.blit(sizeText, (virtualScreenWidth / 2 - 35, virtualScreenHeight / 2 - 85))
        pygame.display.flip

    def drawTheCircles():
        global allPointsList
        line_info('---- Draw button was clicked ----', True)

        circles.screenWidth, circles.screenHeight = screen.get_size()

        for x in range(circles.repeatCountVar.get()):
            pygame.event.pump()
            event = pygame.event.wait()
            line_info('event: ', str(event))
            allPointsList = circles.getAllOfTheArrays()
            if allPointsList[0] == -1:  # An error occurred so abort
                messagebox.showerror(
                    "Error",
                    "An error with circles.getAllOfTheArrays\n"
                )
                return
            if circles.clearBeforeDrawCheckButtonVar.get():
                circles.clearDisplay()
            circles.drawScreenText('Circles',
                                   circles.screenWidth,
                                   circles.screenHeight)
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
                line_info(circles.repeatDelayVar.get())
                pygame.time.wait(circles.repeatDelayVar.get() * 1000)

    # Draw the points
    def drawThePoints():
        line_info("drawThePoints")
        for circlePointsList in allPointsList:
            for aPoint in circlePointsList:
                if circles.foregroundColorRandomCheckButtonVar.get():
                    currentForegroundColor = circles.colorList[
                        random.randrange(0, len(circles.colorList))
                    ]
                else:
                    currentForegroundColor = circles.foregroundColor
                pygame.draw.circle(
                    screen,
                    currentForegroundColor,
                    (aPoint[0], aPoint[1]),
                    circles.pointRadiusVar.get(),
                    circles.lineThicknessVar.get(),
                )

    def drawPointConnectors():
        line_info("drawPointConnectors")
        # pp.pprint(allPointsList)
        for circlePointsList in allPointsList:
            if circles.foregroundColorRandomCheckButtonVar.get():
                currentForegroundColor = circles.colorList[random.randrange(0, len(circles.colorList))]
            else:
                currentForegroundColor = circles.foregroundColor

            for p1, p2 in zip(circlePointsList, circlePointsList[1:]):
                pygame.draw.line(
                    screen, currentForegroundColor, p1, p2, circles.lineThicknessVar.get()
                )

    # Draw connectors between points on the circumference of a circle
    def drawCircleConnectors():  # noqa: C901
        i = 0
        while i < len(allPointsList):
            if circles.twistedLinesCheckButtonVar.get():  # this draws the lines all twisted up
                random.shuffle(allPointsList[i])

            # -1 means random shift amount, 0  no shifting, 1 or more is a shift value
            line_info(circles.shiftedLinesVar.get())
            if circles.shiftedLinesVar.get() == -1:  # random shift amount
                count = random.randint(0, len(allPointsList[i]) - 1)
                x = 0
                while x < count:
                    allPointsList[i].append(allPointsList[i].pop(0))   # left shift
                    # allPointsList[i].insert(0, allPointsList[i].pop())  # right shift
                    x += 1
            elif circles.shiftedLinesVar.get() == 0:  # no shift amount
                pass
            else:
                count = 0
                while count < circles.shiftedLinesVar.get():  # Shift value amount
                    count += 1
                    allPointsList[i].append(allPointsList[i].pop(count))
            i += 1

            j = 0
            while j < len(allPointsList):
                p1 = allPointsList[j]
                j += 1
                if j >= len(allPointsList):
                    break
                p2 = allPointsList[j]

                # Now draw the lines
                k = 0
                while k < len(p1):
                    for circlePointsList in allPointsList:
                        if circles.foregroundColorRandomCheckButtonVar.get():
                            currentForegroundColor = circles.colorList[random.randrange(0, len(circles.colorList))]
                        else:
                            currentForegroundColor = circles.foregroundColor
                    pygame.draw.line(screen, currentForegroundColor,
                                     p1[k], p2[k], circles.lineThicknessVar.get())
                    k += 1

    def clearDisplay():
        screen.fill(circles.backgroundColor)
        pygame.display.flip()
        line_info(' '.join(["clearDisplay:", circles.backgroundColor]))

    def selectBackgroundColor():
        colors = askcolor(title="Background color chooser")
        line_info(' '.join([str(colors[0]), str(colors[1])]))
        if colors[0] is None:  # cancel was selected
            return
        circles.backgroundColor = colors[1]
        screen.fill(circles.backgroundColor)
        pygame.display.flip()
        line_info("selectBackgroundColor")

    def selectforegroundColor():
        colors = askcolor(title="Foreground color chooser")
        line_info(colors[0], colors[1])
        if colors[0] is None:  # cancel was selected
            return
        circles.foregroundColor = colors[1]
        pygame.display.flip()
        line_info("selectforegroundColor")

    def randomBackgroundColor():
        color = random.randrange(0, len(circles.colorList))
        circles.backgroundColor = circles.colorList[color]
        screen.fill(circles.backgroundColor)
        pygame.display.flip()
        line_info(' '.join(["randomBackgroundColor:",
                            str(color),
                            str(circles.backgroundColor)]))


# This is where we loop until user wants to exit
if __name__ == "__main__":
    circles.main()
