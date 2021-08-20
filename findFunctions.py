
import time
import copy
from testsettings import *
from PIL import Image
import cv2
from PIL import ImageDraw
import numpy as np


# and shit and fuck I already did all this. sigh.
framesleep = 0

# for pillow

filename = 'out_IMG_4025.jpg'
#filename = 'sample.png'
img: Image.Image = Image.open(filename)
draw = ImageDraw.Draw(img)

# create a legible demonstration of previously discovered shape.

draw.rectangle([113, 164, 233, 409],None,'red')
draw.rectangle([405, 136, 578, 415],None,'red')

img.save('test.png')

nodisplay = False

# for opencv
cvimg = cv2.imread(filename)


tol = 20
minsize = 15
width, height = img.size
data: list = img.getdata()

if (data.bands > 2):
    raise Exception("This module expects a grayscale image with at most two channels")


# grayscale index where greater than is considered blank
blankthreshold = 90

# this bullshit is what is required to actually
# make a simple wrapper script to test functions
# fucking ridiculous I can't do findfunctions.data = newdata
if (runtests):
    tol = testtol
    minsize = testminsize
    width = testwidth
    height = testheight
    data = testdata
    nodisplay = testnodisplay
    blankthreshold = testblankthreshold

# constants for my very non redundant code idea
UL = 0
LR = 1
XO = 0
YO = 1
DX = 2
DY = 3

shapes = []

def displaythreshhold(threshold):
    newimg = cvimg.copy()

    scany = 0
    scanx = 0

    while scany < height:
        scanx = 0

        while scanx < width:
            if (getpix(scanx,scany) <=threshold):
                cv2.point()


def edgescanhasdata(shape, corner, dimension,dc):
    # upper left corner will ALWAYS be less than LR corner. always.
    # find the constant value for the edge
    # example, if you're considering X, then you're checking a vertical line, which will include the new x position
    dim1 = shape[UL][XO if dimension == YO else YO]
    dim2 = shape[LR][XO if dimension == YO else YO]

    constant = shape[corner][dimension]

    #scanshape = [[dim1 if dimension == YO else constant, constant if dimension == YO else dim1],
    #             [dim2 if dimension == YO else constant, constant if dimension == YO else dim2],
    #             [0, 0]]

    # so lets say I move the left corner, another pixel left, then the line between (ULX,ULY) and (ULX,LRY) is being
    # considered as that is the data we have expanded into.

    while dim1 < dim2 + 1:

        x = dim1 if dimension == YO else constant
        y = constant if dimension == YO else dim1

       # scanshape[2][XO] = x
       # scanshape[2][YO] = y

        #displayShape(shape, f'Scan. Shape:{shape} {dc}')

        # if data is encountered on the new line, return true
        if pixisdata(getpix(x, y)):
            # data found
            return True
        dim1 += 1

    # no data encountered
    return False


def displayShape(shape, banner, scanshape=None):
    if nodisplay:
        return None

    imgcopy = cvimg.copy()


    if (scanshape is not None):
        cv2.line(imgcopy, scanshape[0], scanshape[1], (255, 0, 0, 255))
        cv2.circle(imgcopy, scanshape[2], 1, (0, 0, 255, 255), 1)

    cv2.rectangle(imgcopy, (shape[UL][XO], shape[UL][YO]),
                  (shape[LR][XO], shape[LR][YO]),
                  (0, 255, 0, 255),
                  5
                  )

    aspectration = height / width
    newsize = (900, int(aspectration*900))

    imS = cv2.resize(imgcopy,newsize)

    cv2.putText(imS, banner,
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (0, 255, 0),
                2)

    cv2.imshow('image', imS)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        a = 1


def expandtillnodata(shape, corner, dimension, dc):

    nochange = True

    ori = shape[corner][dimension]

    # keep adjusting a single dimension until no data found
    while edgescanhasdata(shape, corner, dimension, dc):
        if nextstepoutofbounds(shape,corner,dimension):
            break
        shape[corner][dimension] += (-1 if corner == UL else 1) * 1

    # mark where first lack of data was encountered
    firstencounteredno = shape[corner][dimension]

    # copy value for tolerance testing loop
    testo = firstencounteredno

    #restore last good border
    shape[corner][dimension] -= (-1 if corner == UL else 1) * 1

    hasdata = False

    #to minimize scan first copy shape
    newbox= copy.deepcopy( shape)

    newbox[corner][dimension] = firstencounteredno
    # test tolerance rule, expand until tolerance met or data encountered
    #print(f'before tol: {shape}', end='  ')

    while (abs( firstencounteredno - testo ) < tol and not hasdata):

        if (nextstepoutofbounds(newbox,corner,dimension)):
            break
        testo += (-1 if corner == UL else 1) * 1
        newbox[corner][dimension] = testo
        #prior to deepcopy
        #print (f'{newbox} {shape}')
        hasdata = hasdata and edgescanhasdata(newbox, corner, dimension, dc)

    #print(f'after tol: {shape}', end=' ')

    # this means more data was found
    if (hasdata):
        #print(f'data found', end='  ')
        # set the ordinate to the locsted position
        shape[dimension][corner] = testo
        # ok so rule has reset itself, continue

        #print(f'new shape: {shape}')

        shape, nochange = expandtillnodata(shape, corner, dimension)

        #print(f'after shape recall: {shape}')

  #  print()

    nochange = shape[corner][dimension] == ori

    # second part of tuple is true nothing happened.
    return (shape,  nochange )

def nextstepoutofbounds(shape, corner, dimension):
    # if the corner is UL, it will always decrease, so 0 is the leftmost boundary
    # otheriwse the maximum location of data is along the width and height
    # adjust for 1 for zero index
    limit = 0 if corner == UL else (width - 1 if dimension == XO else height - 1)

    # calculate whether this box corner dimension is out of bounds
    # depending on upper left or lower right corner
    return (shape[corner][dimension] - 1 <= limit) \
        if corner == UL else (shape[corner][dimension] + 1 >= limit)


def pixisdata(val):
    return (val <= blankthreshold)


###### helper function to return pixel by x,y
def getpix(x, y):
    if show_test_pixel_value:
        print(data[width * y + x])

    try:
        if (data.bands > 1):
            return data[width * y + x][0]
        else:
            return data[width * y + x]
    except IndexError:
        print('this is where some weird error occurs')
#### finds a shape emanating from a specific point
##### meat of the algorithm to find a shape.
def findshape(x, y):
    # make sure point isnt in another shape.
    for s in shapes:
        if s[UL][XO] <= x <= s[LR][XO] and s[UL][YO] <= y <= s[LR][YO]:
            #print('shape found. leaving findshape')
            return None

    dontchange = [[0, 0], [0, 0]]
    boxpoints = [[x, y], [x, y]]

    proceed = True

    # calculate the and-ed boolean flag indicating whether to keep scanning
    #    for p in [UL, LR]:
    #       for c in [XO, YO]:
    #          proceed = proceed or (dontchange[p][c] == 0)

    while proceed:

        displayShape(boxpoints, f'shape: {boxpoints} dnc: {dontchange}')
        time.sleep(framesleep/1000)

        changes = False

        for corner in [UL, LR]:
            cstr = 'UL' if corner == 'UL' else 'LR'
            #print(f'Corner: {cstr} dc: {dontchange}')
            for dimension in [XO, YO]:
                dstr = 'X' if dimension == XO else 'Y'

                # if a scanline has been marked outofbounds or no data has been
                # encountered in this direction for awhile, don't do anything.
                if dontchange[corner][dimension] == 0:
             #       print(f'Dim: {dstr}')
                    # mark dimension for no adjustment if a modification would put it out of bounds
                    if nextstepoutofbounds(boxpoints, corner, dimension):
                        #print('result: out of bounds')
                        dontchange[corner][dimension] = 1
                    else:

                       # print(f'entered expand at: {boxpoints} and dc:{dontchange}')
                        boxpoints, nochange = expandtillnodata(boxpoints, corner, dimension, dontchange)
                        #print(f'left expand at: {boxpoints}')
                        dontchange[corner][dimension] = 1

                        if not nochange:
                            # if you expanded a row or column there is a possibility
                            # that changing the other direction will expand tp
                            # new data that could not be reached before.
                            dontchange[UL][XO if dimension == YO else YO] = \
                               1 if nextstepoutofbounds(boxpoints, UL, XO if dimension == YO else YO) \
                                   else 0

                            dontchange[LR][XO if dimension == YO else YO] = \
                                1 if nextstepoutofbounds(boxpoints, LR, XO if dimension == YO else YO) \
                                    else 0

        # jesus.
        proceed = False

        # calculate the and-ed boolean flag indicating whether to keep scanning
        for corner in [UL, LR]:
            for dimension in [XO, YO]:
                proceed = proceed or (dontchange[corner][dimension] == 0)

    #print('===> leaving scanobject')

    if (boxpoints[LR][XO] - boxpoints[UL][XO] >= minsize or
            boxpoints[LR][YO] - boxpoints[UL][YO] >= minsize):
        return boxpoints
    else:
        return None
