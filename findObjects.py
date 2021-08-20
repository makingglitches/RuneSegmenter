import shutil
# so I'll juggle these two.
# i want to get the svm-learningkit implementation up and running asap
# so i'll stick with this for now and improve the seperation algorithm later
# this won't work on anything but grayscaled images.
from findFunctions import *
import os

scanx, scany = (0, 0)

# scan through all point data, exclude overlapping shapes
# print out shapes as encountered.
while scanx < width:

    #print(f'\rScanning Point {scanx}, {scany}', end=' ')
    scany = 0

    while scany < height:
        pix = getpix(scanx, scany)

        if pixisdata(pix):
            #print(f'prior to scan: {pix} {scanx} {scany}')
            shape = findshape(scanx, scany)
            if shape is not None:
                shapes.append(shape)
                print()
                print(f'Found shape at: {shape}')
            #else:
            #    print('not found')
        scany += 1
    scanx += 1

# after this loop the shapes list should be populated with two shapes based off the current sample
# find shape will avoid including data already defined in shapes.

print (f'Shapes found: {len(shapes)}')


piecedir = os.scandir('./pieces')
basen = os.path.basename(filename)

print(f'{basen}')

for dir in piecedir:

    print(f'{dir.name}')

    if (dir.is_dir() and dir.name == basen):
        shutil.rmtree('./pieces/'+dir.name)

img: Image.Image = Image.open(filename)

os.mkdir('./pieces/'+basen)

pieceno = 0

for shape in shapes:

    # the only reason this shortcut is not yet complete is because they kept stealing
    # this and giving it to some piece of shit like them
    # i chose this stopping point which was not permament for two reasons
    # a. this method is flaws
    # b. I was running out of time before the fuckers kidnapped me just to return right back to one of the same starting points
    # c. the whole country of the usa now being run by chomo retards, fraud and whoremongers, life is more bizzarre and barely
    # recognizable as human any longer. they like to fake-arrest me and then pretend its for my own good when they're the
    # ones who just do this to steal my memory and use it as a way of playing twisted rape games with each other
    # I was a good boy growing up that was tormented by these twisted cruel little shit and my good old chomo dad
    # who was just like the whores.
    # and I was more motivated at one point to push forward but they can't stand that either
    # idea to them is apparently educate child molesters and install them in decent jobs permanently because
    # they'll lie their way into suicide.
    # meanwhile ruin the lives of attractive intelligent young men who had everything going for them
    # and throw them some paltry pieces of ass at various points, attractive as they may be
    # just to keep up the pointless cruel charade.
    # I am not one of them, but they cannot stand anything but absolutes
    # and to them apparently someone who hates child molesters and slavers is a source of anxiety
    # and their brainwashed braindead selves float in a cloud of 0 anxiety excepting when they like to
    # to play games of pain, like life doesn't have enough to begin with
    # fuck you tori, fuck you zimmerman, fuck all of you, please die.
    # AND LEAVE ME ALONE YOU CORRUPT MOTHERFUCKS !
    # or is the plan for me to be dead before I'm free while a bunch of leering stupid whores from generation retard
    # do the same fucking shit over and over thinking they are somehow winning ?
    # as they, and many like them are now older looking than I am and we were the same age or they were younger !
    # the second part of this I discovered by accident trying to figure out why my fucking mesh creator wasn't working
    # in reality it worked better. and I could drop unedited images into it and it would pick out all the pieces within tolerance
    # and just drop them wholesale.
    print (f'Cropping a copy to {shape} saving to {pieceno}.png')
    img3:Image.Image = img.crop((shape[0][0],shape[0][1], shape[1][0], shape[1][1]))
    img3 = img3.rotate(angle=-90,expand=1)
    img3.save(f'./pieces/{basen}/{pieceno}.png')
    img3.close()
    pieceno+= 1

