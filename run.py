import lemonadeImage

x = lemonadeImage.lemonadeImage()
x.loadImage('mountain.bmp')

xE = x.cornerDetectFAST(80)

xN = lemonadeImage.lemonadeImage()
xN.setSize(x.width() - 6, x.height() - 6)
xN.setBpp(24)

xN.setPixelAll((0,0,0))

for i in xE:
    xN.setPixel(i[0] - 3,i[1] - 3,(255,255,255))

xN.saveImage('bmp4.bmp')

xN = x.edgeDetectSobel()
xN.setBpp(24)
xN.saveImage('bmp5.bmp')